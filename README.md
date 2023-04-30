
# Steam-producer

Requiredment
- Python >= 3.8




## Installation

Create environment and install all dependency

```bash
  pythom3 -m venv venv
  cd stream_producer
  source venv/bin/activate
  pip3 install -r requiredment.txt

```

## Run
Have to start rtsp-simple server with docker on your computer ,labtop, etc

```bash
docker run --rm -it -e RTSP_PROTOCOLS=tcp -p 8554:8554 -p 1935:1935 -p 8888:8888 -p 8889:8889 aler9/rtsp-simple-server

```

Run steam-producer
```bash
cd stream_producer
sorce venv/bin/activate

## python3 stream_producer.py --path <your_path_to_rtsp-simple-server> --src <camera_device>

python3 stream_producer.py --path test --src 0

```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`RTSP_ADDRESS=rtsp://<address>:<port>/`


