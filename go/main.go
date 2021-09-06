package main

import (
	"fmt"
	"io"
	"net"
	"net/http"
	"time"

	"github.com/hashicorp/go-retryablehttp"
)

func main() {
	connectTimeout := time.Millisecond * 15000
	tlsHandshakeTimeout := time.Millisecond * 10000
	respHdrReadTimeout := time.Millisecond * 5000
	idleTimeout := time.Millisecond * 20000
	requestTimeout := time.Millisecond * 30000

	httpClient := http.Client{
		Transport: &http.Transport{
			DialContext: (&net.Dialer{
				Timeout:   connectTimeout,
				KeepAlive: connectTimeout,
			}).DialContext,
			TLSHandshakeTimeout:   tlsHandshakeTimeout,
			ResponseHeaderTimeout: respHdrReadTimeout,
			IdleConnTimeout:       idleTimeout,
		},
		Timeout: requestTimeout,
	}

	client := retryablehttp.Client{
		HTTPClient: &httpClient,
		RetryMax:   3,
		CheckRetry: retryablehttp.DefaultRetryPolicy,
		Backoff:    retryablehttp.DefaultBackoff,
	}

	response, err := client.Get("https://en.wikipedia.org/w/api.php")
	if err != nil {
		fmt.Println("Error in Fetching Data", err)
		return
	}

	defer response.Body.Close()

	body, err := io.ReadAll(response.Body)
	if err != nil {
		fmt.Println("Error in Reading Response Body", err)
		return
	}

	fmt.Println("Response Text =", string(body))
}
