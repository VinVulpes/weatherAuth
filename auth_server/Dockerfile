FROM golang
WORKDIR /authserver/
COPY ./go.mod/ ./go.sum ./
RUN go mod download
COPY . .
RUN go build -o ./auth_server.bin ./auth_server.go
CMD [ "bash", "-c", "./auth_server.bin"]
