#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include "x_control/pid.hpp"

// Recibe el setpoint de navegacion y la odometria, publica el esfuerzo de los 6 thrusters
class PidController : public rclcpp::Node {
public:
  PidController() : Node("pid_controller"),
    depth_pid_(declare_parameter("depth.kp", 2.0), declare_parameter("depth.ki", 0.1), declare_parameter("depth.kd", 0.5)),
    yaw_pid_(declare_parameter("yaw.kp", 1.5), declare_parameter("yaw.ki", 0.0), declare_parameter("yaw.kd", 0.3)) {
    setpoint_sub_ = create_subscription<geometry_msgs::msg::PoseStamped>(
      "/x/control/setpoint", 10, [this](geometry_msgs::msg::PoseStamped::SharedPtr msg) { setpoint_ = *msg; });
    odom_sub_ = create_subscription<nav_msgs::msg::Odometry>(
      "/x/odom", 10, [this](nav_msgs::msg::Odometry::SharedPtr msg) { odom_ = *msg; });
    thrust_pub_ = create_publisher<std_msgs::msg::Float64MultiArray>("/x/thrusters/cmd", 10);
    timer_ = create_wall_timer(std::chrono::milliseconds(50), [this]() { step(); });
  }

private:
  void step() {
    const double dt = 0.05;
    double depth_err = setpoint_.pose.position.z - odom_.pose.pose.position.z;
    double heave = depth_pid_.update(depth_err, dt);
    // TODO: el yaw no se calcula todavia, se manda 0
    double yaw = yaw_pid_.update(0.0, dt);
    std_msgs::msg::Float64MultiArray cmd;
    cmd.data = {yaw, -yaw, yaw, -yaw, heave, heave};
    thrust_pub_->publish(cmd);
  }

  x_control::Pid depth_pid_;
  x_control::Pid yaw_pid_;
  geometry_msgs::msg::PoseStamped setpoint_;
  nav_msgs::msg::Odometry odom_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr setpoint_sub_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr thrust_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PidController>());
  rclcpp::shutdown();
  return 0;
}
