package main

import (
	"authServer/pkg/api"
	"context"
	"log"
	"net"

	"google.golang.org/grpc"
)

//структура сервера и обьявление хеш-таблицы
type grpcServer struct {
	api.AuthServiceServer
	userTable map[string]bool
}

func (s grpcServer) CheckAuthorization(ctx context.Context, req *api.AuthRequest) (*api.AuthResponse, error) {
	username := req.GetUserName() //берем username
	if _, ok := s.userTable[username]; ok {
		return &api.AuthResponse{IsAuthorized: true}, nil
	}
	return &api.AuthResponse{IsAuthorized: false}, nil
}

func (s grpcServer) mustEmbedUnimplementedMessageServer() {
	log.Fatal("Всё плохо...")
}

func main() {
	userTable := make(map[string]bool)
	//Таблица пользователей
	userTable["user1"] = true
	userTable["Shepard"] = true
	userTable["Grunt"] = true
	userTable["Miranda"] = true
	s := &grpcServer{userTable: userTable}
	// создаем gRPC-сервер
	srv := grpc.NewServer()
	api.RegisterAuthServiceServer(srv, s)
	//запускаем на 9000 порту
	lis, err := net.Listen("tcp", ":9000")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	log.Println("auth service started")
	if err := srv.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
