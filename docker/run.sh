xhost +local:root

#TODO change output/input maping
IMAGE="deepstream_yolo_py"
CONTAINER="aa_DeepstreamYoloPy"
OUTPUT_PATH="output.mp4"
SCRIPT_NAME = "deepstream_aa_test.py"


docker stop $CONTAINER || true && docker rm $CONTAINER || true

sudo docker run -it \
	--rm \
	--net=host \
	--runtime nvidia \
	--privileged=true \
	--volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
	# -e DISPLAY \
	-v /tmp/.X11-unix/:/tmp/.X11-unix \
	--name CONTAINER \
	$IMAGE \
	python3 deepstream_aa_test.py

