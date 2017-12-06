#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <vector>
#include <iostream>
#include <utility>

using namespace cv;

std::vector<std::vector<int>> getMovement(Mat frame){
	std::vector<std::vector<int>> count(8, std::vector<int>(8, 0)); // vector of squares
	float threshold = 10.0f; // how sensitive of a movement we need
	int index1 = frame.rows / 8;
	int index2 = frame.cols / 8;

  // how many pixels reached the threshold
	for(int j = 0; j<frame.rows; j++){
	  for(int i = 0; i < frame.cols; i++){
		  if(frame.at<uchar>(j,i) > threshold){
			  count[j /index1][i/ index2]++;
		  }
	  }
	}
	return count;
}
void draw(std::vector<std::vector<int>> matrix, Mat frame){
    // draws the rectangles and the circles
    for(int i = 0; i<8; i++){
    	for(int j = 0; j<8; j++){
		    rectangle(frame,
	        Point(frame.size().width*j/8, frame.size().height*i/8),
		      Point(frame.size().width*(j+1)/8, frame.size().height*(i+1)/8),
		      Scalar(0,255,255));

		    ellipse(frame,
		      Point(frame.size().width*(j+0.5)/8, frame.size().height*(i+0.5)/8),
		      Size((frame.size().width/8)*((float)matrix[i][j]/((frame.size().width/8)*(frame.size().height/8)*2)), (frame.size().height/8)*((float)matrix[i][j]/((frame.size().width/8)*(frame.size().height/8)*2))),
		      0,
		      0,
		      360,
		      Scalar(0,0,255),
		      2,
		      8);
	     }
    }
}

int main(int argc, char* argv[]){
  VideoCapture cap(argv[1]);     // get 'any' cam
  Mat prevFrame, d1;
  
  // initial frame capture
  if(cap.isOpened()){
  	cap.read(prevFrame);
	  cvtColor(prevFrame, prevFrame, CV_BGR2GRAY);
  }

  while( cap.isOpened() ){
    Mat frame, colorFrame;
    // grab the current frame
    if ( ! cap.read(frame) )
      break;

	  Mat dst;
	  int flipAxis;

    // determine axis for flip
	  if(argv[1][10] == '0'){
		  flipAxis = 0;
	  }else{
		  flipAxis = 1;
  	}
  
    flip(frame,dst,flipAxis);
	  frame = dst;
    colorFrame = frame;
	  cvtColor(frame, frame, CV_BGR2GRAY); // convert from BGR to Greyscale
	  absdiff(frame, prevFrame, d1); // find the difference between current and previous frames
	  std::vector<std::vector<int>> result = getMovement(d1); 

	  cvtColor(d1, d1, CV_GRAY2BGR);
    draw(result, d1); // draw the circles
	  draw(result, colorFrame);

    imshow("Grey Detection", d1); // pixel differencing stream
	  imshow("Actual Stream", colorFrame); // actual stream
	  prevFrame = frame;

    // wait for key to terminate
    int k = waitKey(1);
    if ( k==27 )
      break;
  }
  return 0;
}
