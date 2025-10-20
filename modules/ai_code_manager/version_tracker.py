if __name__ == "__main__":version: "3.8"
services:
  sorisae:
    image: parkcheolhong/sorisae:v1
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5050:5050"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    update_version()
