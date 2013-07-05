# /usr/bin/env python
'''
Script to process all the videos in a directory and create the tags for embedding into the course.

Requires "ffprobe": http://ffmpeg.org/ffprobe.html

'''
import os, time, sys, math
import argparse, hashlib, subprocess


def run(input_dir,output_file):
    MEDIA_TYPES = ['.avi','.m4v','.mp4']
    print 'Starting scanning: ' + input_dir
    
    try:
        os.listdir(input_dir)
    except OSError:
        print "Not a valid directory"
        return
    
    out_file = open(output_file, 'w')
    for filename in os.listdir(input_dir):
        for media_type in MEDIA_TYPES:
            if filename.endswith(media_type):
                out_file.write(filename +":\n")
                out_file.write("------------------------------------------\n")
                file_size = os.path.getsize(os.path.join(input_dir,filename ))
                md5sum = md5Checksum(os.path.join(input_dir,filename ))
                file_length = getLength(os.path.join(input_dir,filename ))
                tag_string = "[[media object='{\"filename\":\"%s\",\"download_url\":\"<INSERT_FULL_URL_HERE>/%s\",\"digest\":\"%s\", \"filesize\":%d, \"length\":%d}']]IMAGE/TEXT HERE[[/media]]"
                out_file.write(tag_string % (filename, filename, md5sum, file_size, file_length))
                out_file.write("\n\n")
                print "Processed: "+filename
                
    out_file.close()
    
    print 'finished'

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def getLength(filename):
  result = subprocess.Popen(["ffprobe", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  duration_list = [x for x in result.stdout.readlines() if "Duration" in x]
  time_components = duration_list[0].split(',')[0].split(':')
  hours = int(time_components[1])
  mins = int(time_components[2])
  secs = math.floor(float(time_components[3]))
  video_length = (hours*60*60) + (mins*60) + secs
  return int(video_length)
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Input directory")
    parser.add_argument("output", help="Output file")
    args = parser.parse_args()
    run(args.directory,args.output)
