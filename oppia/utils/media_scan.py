# /usr/bin/env python
'''
Script to process all the videos in a directory and create the tags for 
embedding into the course.

For full instructions, see the documentation at 
https://oppiamobile.readthedocs.org/en/latest/

Requires "ffprobe": http://ffmpeg.org/ffprobe.html

'''

import os, time, sys, math, gst
import argparse, hashlib, subprocess
import Image

def run(input_dir, output_dir, image_width, image_height):
    MEDIA_TYPES = ['.avi','.m4v','.mp4']
    print 'Starting scanning: ' + input_dir
    
    try:
        os.listdir(input_dir)
    except OSError:
        print "Not a valid directory"
        return
    
    out_file = open(os.path.join(output_dir,'output.txt' ), 'w')
    directory_list = os.listdir(input_dir)
    directory_list.sort()
    for filename in directory_list:
        for media_type in MEDIA_TYPES:
            if filename.endswith(media_type):
                out_file.write(filename +":\n")
                out_file.write("------------------------------------------\n")
                file_size = os.path.getsize(os.path.join(input_dir,filename ))
                md5sum = md5_checksum(os.path.join(input_dir,filename ))
                print os.path.join(input_dir,filename )
                file_length = get_length(os.path.join(input_dir,filename ))
                tag_string = "[[media object='{\"filename\":\"%s\",\"download_url\":\"<INSERT_FULL_URL_HERE>/%s\",\"digest\":\"%s\", \"filesize\":%d, \"length\":%d}']]IMAGE/TEXT HERE[[/media]]"
                out_file.write(tag_string % (filename, filename, md5sum, file_size, file_length))
                out_file.write("\n\n")
                print "Processed: "+filename
                
                # create directory for the frame images from video
                print os.path.join(output_dir, filename + ".images")
                if not os.path.exists(os.path.join(output_dir, filename + ".images")):
                    os.makedirs(os.path.join(output_dir, filename + ".images"))
                    
                image_generator_command = "ffmpeg -i %s -r 0.02 -s %dx%d -f image2 %s/frame-%%03d.png" % (os.path.join(input_dir, filename), image_width, image_height, os.path.join(output_dir, filename + ".images")) 
                print image_generator_command
                subprocess.call(image_generator_command, shell=True)  
    out_file.close()
    
    print 'finished'

def md5_checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def get_length(filename):
    result = subprocess.Popen(["avprobe", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    duration_list = [x for x in result.stdout.readlines() if "Duration" in x]
    time_components = duration_list[0].split(',')[0].split(':')
    hours = int(time_components[1])
    mins = int(time_components[2])
    secs = math.floor(float(time_components[3]))
    video_length = (hours*60*60) + (mins*60) + secs
    return int(video_length)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory", help="Input directory")
    parser.add_argument("output_directory", help="Output directory")
    parser.add_argument("-W","--image_width", help="width of image file to create",type=int)
    parser.add_argument("-H","--image_height", help="height of image file to create",type=int)
    args = parser.parse_args()
    run(args.input_directory,args.output_directory,args.image_width,args.image_height)
