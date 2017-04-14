;; Auto-generated. Do not edit!


(when (boundp 'coffebot::MakeVideoGoal)
  (if (not (find-package "COFFEBOT"))
    (make-package "COFFEBOT"))
  (shadow 'MakeVideoGoal (find-package "COFFEBOT")))
(unless (find-package "COFFEBOT::MAKEVIDEOGOAL")
  (make-package "COFFEBOT::MAKEVIDEOGOAL"))

(in-package "ROS")
;;//! \htmlinclude MakeVideoGoal.msg.html


(defclass coffebot::MakeVideoGoal
  :super ros::object
  :slots (_make_video_command ))

(defmethod coffebot::MakeVideoGoal
  (:init
   (&key
    ((:make_video_command __make_video_command) (instance coffebot::MakeVideo :init))
    )
   (send-super :init)
   (setq _make_video_command __make_video_command)
   self)
  (:make_video_command
   (&rest __make_video_command)
   (if (keywordp (car __make_video_command))
       (send* _make_video_command __make_video_command)
     (progn
       (if __make_video_command (setq _make_video_command (car __make_video_command)))
       _make_video_command)))
  (:serialization-length
   ()
   (+
    ;; coffebot/MakeVideo _make_video_command
    (send _make_video_command :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; coffebot/MakeVideo _make_video_command
       (send _make_video_command :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; coffebot/MakeVideo _make_video_command
     (send _make_video_command :deserialize buf ptr-) (incf ptr- (send _make_video_command :serialization-length))
   ;;
   self)
  )

(setf (get coffebot::MakeVideoGoal :md5sum-) "fa6b65ac1fe287cb8e878d75616abc7c")
(setf (get coffebot::MakeVideoGoal :datatype-) "coffebot/MakeVideoGoal")
(setf (get coffebot::MakeVideoGoal :definition-)
      "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
#goal
MakeVideo make_video_command

================================================================================
MSG: coffebot/MakeVideo
#message for command to make video

bool start_video
int8 duration #duration in seconds
string video_file_name

")



(provide :coffebot/MakeVideoGoal "fa6b65ac1fe287cb8e878d75616abc7c")

