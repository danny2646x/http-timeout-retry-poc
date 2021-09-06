require 'faraday'

puts "Starting API Retry POC...."

## Retry Exception ##
class RetryError < StandardError
    def message
      "All Retries Exhausted!!"
    end
end

## Retry Configuration ##
retry_options = {
    max: 5,
    interval: 0.05,
    interval_randomness: 0.5,
    backoff_factor: 2,
    methods: %i[get options head delete post put],
    exceptions: [Faraday::TimeoutError, Faraday::ConnectionFailed, Faraday::RetriableResponse],
    retry_statuses: [404, 429, 503, 502, 504, 500],

    ## Define this Block to catch Exhausted Retries Error
    retry_block: -> (env, options, retries, exc) { 
        puts "Entering the Retry Block... Use this for Logging Purposes"
        printf "Response Status Code = %d\n", env.status
        printf "Available Retries = %d\n", retries
        printf "Exception Class = #{exc.class}: Exception Message = #{exc.message}"
        puts "Exitting the Retry Block..."
 
        raise RetryError unless retries > 0
    }
}

## Connection ##
conn = Faraday.new(
    url: 'http://httpbingo.org',
    params: {param: '1'},
    headers: {'Content-Type' => 'application/json'},
    request: {timeout: 1}
) do |f|
    f.request :retry, retry_options
end

## Driver ##
begin
    response = conn.get('/status/404')
    printf "Response Status = %s\n", response.status
    printf "Response Headers = %s\n", response.headers
    printf "Response Body = %.100s\n", response.body
rescue Faraday::TimeoutError => e
    printf "Request Timeout Out!! Exception Class = #{e.class}: Exception Message = #{e.message}"
rescue RetryError => e
    printf "Retry Failed!! Exception Class = #{e.class}: Exception Message = #{e.message}"
rescue => e
    printf "Request Error!! Exception Class = #{e.class}: Exception Message = #{e.message}"
end


puts "Exitting API Retry POC...."
