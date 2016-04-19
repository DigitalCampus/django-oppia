# /usr/bin/env python
'''
Script to process all the videos in a directory and create the tags for 
embedding into the course.

For full instructions, see the documentation at 
https://oppiamobile.readthedocs.org/en/latest/

Requires "ffprobe": http://ffmpeg.org/ffprobe.html

'''

import os, time, sys, math
import argparse, hashlib, subprocess

DEFAULT_WIDTH = 320
DEFAULT_HEIGHT = 180

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def run(input_dir, output_dir, image_width=DEFAULT_WIDTH, image_height=DEFAULT_HEIGHT):
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
    processed = 1
    for filename in directory_list:
        for media_type in MEDIA_TYPES:
            if filename.endswith(media_type):
                out_file.write("\n"+filename +":\n\n")
                file_size = os.path.getsize(os.path.join(input_dir,filename ))
                md5sum = md5_checksum(os.path.join(input_dir,filename ))

                print "Processing " + bcolors.BOLD + filename + bcolors.ENDC + " (" + str(processed) + "/" + str(len(directory_list)) + "):"
                file_length = get_length(os.path.join(input_dir,filename ))
                tag_string = "[[media object='{\"filename\":\"%s\",\"download_url\":\"FULL_URL/%s\",\"digest\":\"%s\", \"filesize\":%d, \"length\":%d}']]IMAGE/TEXT HERE[[/media]]"
                out_file.write(tag_string % (filename, filename, md5sum, file_size, file_length))
                out_file.write("\n\n")
                print "  > Processed metadata."

                # create directory for the frame images from video

                if not os.path.exists(os.path.join(output_dir, filename + ".images")):
                    os.makedirs(os.path.join(output_dir, filename + ".images"))
                print "  > Created output dir " + os.path.join(output_dir, filename + ".images")

                print "  > Generating miniatures... \r",
                image_generator_command = "ffmpeg -i %s -r 0.02 -s %dx%d -f image2 %s/frame-%%03d.png" % (os.path.join(input_dir, filename), image_width, image_height, os.path.join(output_dir, filename + ".images"))
                #print image_generator_command
                ffmpeg = subprocess.Popen(image_generator_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                currentFrame = 0
                for line in iter(ffmpeg.stdout.readline,''):
                    if "frame=" in line:
                        if line.split(" ")[3] is "":
                            frame = int(line.split(" ")[4])
                        else:
                            frame = int(line.split(" ")[3])
                        if frame > currentFrame:
                            currentFrame = frame
                            print "  > Generating miniatures... " + str(frame*10) + "% \r",
                            #sys.stdout.write(str(frame*10) + "% ... ")
                print "  > Generating miniatures... 100% \r",
                print "\n  > Process completed."
        processed += 1

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
    if args.image_height is None:
        args.image_height = DEFAULT_HEIGHT
    if args.image_width is None:
        args.image_width = DEFAULT_WIDTH
    run(args.input_directory,args.output_directory,args.image_width,args.image_height)
