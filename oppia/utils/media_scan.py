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

def run(input_dir,output_dir,no_frames,image_max_width):
    MEDIA_TYPES = ['.avi','.m4v','.mp4']
    print 'Starting scanning: ' + input_dir
    
    try:
        os.listdir(input_dir)
    except OSError:
        print "Not a valid directory"
        return
    
    out_file = open(os.path.join(output_dir,'output.txt' ), 'w')
    for filename in os.listdir(input_dir):
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
                
                # create some image files for video
                frame_filename = "%s-frame-%02d.png"
                '''
                split = int(file_length/(no_frames+1))
                for i in range(1,(no_frames+1)):
                    buf = get_frame_image(os.path.join(input_dir,filename),i*split)
                    image_filename = os.path.join(output_dir,frame_filename % (filename,i))
                    with file(image_filename, 'w') as fh:
                        fh.write(str(buf))
                      
                    # now resize the image
                    img = Image.open(image_filename)
                    wpercent = (image_max_width / float(img.size[0]))
                    hsize = int((float(img.size[1]) * float(wpercent)))
                    img = img.resize((image_max_width, hsize), Image.ANTIALIAS)
                    img.save(image_filename)  
                    print "Created frame image %02d at %d secs" % (i, i*split)
                ''' 
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
  
def get_frame_image(path, offset=5, caps=gst.Caps('image/png')):
    pipeline = gst.parse_launch('playbin2')
    pipeline.props.uri = 'file://' + os.path.abspath(path)
    pipeline.props.audio_sink = gst.element_factory_make('fakesink')
    pipeline.props.video_sink = gst.element_factory_make('fakesink')
    pipeline.set_state(gst.STATE_PAUSED)
    # Wait for state change to finish.
    pipeline.get_state()
    assert pipeline.seek_simple(
        gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, offset * gst.SECOND)
    # Wait for seek to finish.
    pipeline.get_state()
    buffer = pipeline.emit('convert-frame', caps)
    pipeline.set_state(gst.STATE_NULL)
    return buffer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory", help="Input directory")
    parser.add_argument("output_directory", help="Output directory")
    parser.add_argument("-f","--frames", help="number of frames to create", type=int,default=5)
    parser.add_argument("-w","--image_max_width", help="max width of image file to create",type=int,default=250)
    args = parser.parse_args()
    run(args.input_directory,args.output_directory,args.frames,args.image_max_width)
