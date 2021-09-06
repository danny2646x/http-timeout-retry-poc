package main

import (
	"net/http"
	"time"
)

// Default Timeouts
const (
	DefaultDialTimeoutMs   = 100000
	DefaultSocketTimeoutMs = 10000
	DefaultRetryCount      = 3
	DefaultBackoffFactor   = 0
)

type Request struct {
	httpClient    *http.Client
	dialTimeout   time.Duration
	socketTimeout time.Duration
	maxRetryCount int
	backOffFactor float64
}

func NewRequest() *Request {
	return &Request{
		dialTimeout:   time.Millisecond * DefaultDialTimeoutMs,
		socketTimeout: time.Millisecond * DefaultSocketTimeoutMs,
		maxRetryCount: DefaultRetryCount,
		backOffFactor: DefaultBackoffFactor,
		httpClient:    &http.Client{},
	}
}

func (r *Request) WithRetries(retryCount int) *Request {
	r.maxRetryCount = retryCount
	return r
}

func (r *Request) WithDialTimeout(dialTimeout time.Duration) *Request {
	r.dialTimeout = dialTimeout
	return r
}

func (r *Request) WithSocketTimeout(socketTimeout time.Duration) *Request {
	r.socketTimeout = socketTimeout
	return r
}
