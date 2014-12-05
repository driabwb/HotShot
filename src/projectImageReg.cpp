/* 

   Andy McEvoy
   michael.mcevoy@colorado.edu

   12 - June - 2013

   Converts a ROS image stream into an OpenCV image stream

*/

#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <vector>
#include <std_msgs/Point.h>

// Message
#include <project/centeringDirection.h>

using namespace std;
using namespace cv;

namespace enc = sensor_msgs::image_encodings;

static const char WINDOW[] = "OpenCV Image";

int global_min_threshold=50;
int global_squareness_ratio=60;

void update_global_min_threshold(int,void*) {
  //do nothing
}

void update_global_squareness_ratio(int,void*) {
  //do nothing
}

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;
  float minDist;
  int param1, param2, minRadius, maxRadius;
  std_msgs::Point centering_msg;
  ros::Publisher centering_pub;
  
public:
  ImageConverter(char* ros_image_stream, float min_dist, int param_1, int param_2, int min_radius, int max_radius)
    : it_(nh_)
  {

    image_pub_ = it_.advertise("correll_ros2opencv", 1);
    image_sub_ = it_.subscribe(ros_image_stream, 1, &ImageConverter::imageCb, this);

    centering_pub = Publisher("centering_msg", centering_msg);
    nh_.publish(centering_pub);


    this->minDist = min_dist;
    this->param1 = param_1;
    this->param2 = param_2;
    this->minRadius = min_radius;
    this->maxRadius = max_radius;

    cv::namedWindow(WINDOW);
  }

  ~ImageConverter()
  {
    cv::destroyWindow(WINDOW);
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    cv_bridge::CvImagePtr cv_ptr;
    try
      {
    cv_ptr = cv_bridge::toCvCopy(msg, enc::BGR8);
      }
    catch (cv_bridge::Exception& e)
      {
    ROS_ERROR("cv_bridge exception: %s", e.what());
    return;
      }

    /* Add any OpenCV processing here */
    /* Gray scale image */
    cv::Mat filtered_image;
    cv::cvtColor(cv_ptr->image,filtered_image,CV_BGR2GRAY);
    //    cv::GaussianBlur(filtered_image,filtered_image,cv::Size(9,9), 2, 2);

    // Show final filtered image 
    cv::namedWindow("Filtered Image");
    cv::imshow("Filtered Image",filtered_image);


    vector<cv::Vec3f> circles;
    minDist = filtered_image.rows/8;
    /// Apply the Hough Transform to find the circles
    cv::HoughCircles( filtered_image, circles, CV_HOUGH_GRADIENT, 1, minDist, param1, param2, minRadius, maxRadius);
    
    Point imageCenter(cvRound(filtered_image.cols/2), cvRound(filtered_image.rows/2));
    circle( filtered_image, imageCenter, 3, Scalar(0,255,0), -1, 8, 0 );

    FILE* outputFile = fopen("data.txt", "a");

    /// Draw the circles detected
    for( size_t i = 0; i < circles.size(); i++ )
      {
	Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
	int radius = cvRound(circles[i][2]);

	// Log where the circle is
	fprintf(outputFile, "(%i, %i), %i\n", center.x, center.y, radius);

	// Message how to move baxter
	centering_msg.x = imageCenter.x - center.x;
	centering_msg.y = imageCenter.y - center.y;
	centering_pub.publish(&centering_msg);
	nh_.spinOnce();

	// circle center
	circle( filtered_image, center, 3, Scalar(0,255,0), -1, 8, 0 );
	// circle outline
	circle( filtered_image, center, radius, Scalar(0,0,255), 3, 8, 0 );
      }
    
    fclose(outputFile);
    
    // Pass a message to elsewhere to control baxter
    


    /// Show your results
    namedWindow( "Hough Circle Transform Demo", CV_WINDOW_AUTOSIZE );
    imshow( "Hough Circle Transform Demo", filtered_image );

    // end of processing
    // cv::imshow(WINDOW, cv_ptr->image);
    cv::waitKey(3);
    
    image_pub_.publish(cv_ptr->toImageMsg());
  }
};

int main(int argc, char** argv)
{
  if (argc==2) {
    ros::init(argc, argv, "correll_image_converter");
    ImageConverter ic(argv[1], 0.0, 200, 100, 0, 50);
    ros::spin();
    return 0;
  } else {
    std::cout<<"ERROR:\tusage - RosToOpencvImage <ros_image_topic>"<<std::endl;
    return 1;
  }
}
