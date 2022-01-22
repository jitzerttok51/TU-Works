package main

import (
	"errors"
	"flag"
	"fmt"
	"log"
)

func main() {

	args, err := retriveArgs()

	if err != nil {
		log.Println(err)
		flag.CommandLine.Usage()
		return
	}

	K := args.key
	text := args.text
	ks := keyStream(K)

	if args.op == encryption {
		ecrypted := encrypt(ks)(text)
		fmt.Println(ecrypted)
	}

	if args.op == decryption {
		plain := decrypt(ks)(text)
		fmt.Println(plain)
	}
}

func keyStream(K string) [256]uint8 {
	var S [256]uint8
	for i := 0; i < len(S); i++ {
		S[i] = uint8(i)
	}

	j := 0
	for i := 0; i < len(S); i++ {
		j = (j + int(S[i]) + int(K[i%len(K)])) % 256
		tmp := S[i]
		S[i] = S[j]
		S[j] = tmp
	}

	return S
}

func encrypt(K [256]uint8) func(string) string {
	return func(plaintext string) string {
		var cyphertext = make([]uint8, len(plaintext))
		for i := 0; i < len(plaintext); i++ {
			k := K[i%len(K)]
			v := plaintext[i]
			cyphertext[i] = k ^ v
		}

		return string(cyphertext)
	}
}

func decrypt(K [256]uint8) func(string) string {
	return func(cyphertext string) string {
		var plaintext = make([]uint8, len(cyphertext))
		for i := 0; i < len(plaintext); i++ {
			k := K[i%len(K)]
			v := cyphertext[i]
			plaintext[i] = k ^ v
		}

		return string(plaintext)
	}
}

type operation int

const (
	encryption operation = iota
	decryption
)

type arguments struct {
	text string
	key  string
	op   operation
}

func retriveArgs() (arguments, error) {

	operation := flag.String("operation", "encrypt", "Select an operation mode for the algorithm. Possible options: \"decrypt\", \"encrypt\"")
	key := flag.String("key", "", "Key for the selcted operation")
	text := flag.String("text", "", "Text fo the selected operation")

	flag.Parse()

	var args arguments

	switch *operation {
	case "encrypt":
		args.op = encryption
	case "decrypt":
		args.op = decryption
	default:
		return args, errors.New("operation paramerter must be  \"decrypt\" or \"encrypt\"")
	}

	if *key == "" {
		return args, errors.New("key parameter must not be empty")
	}
	args.key = *key

	if *text == "" {
		return args, errors.New("text parameter must not be empty")
	}
	args.text = *text

	return args, nil
}
