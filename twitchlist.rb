#!/usr/bin/env ruby

require 'net/http'
require 'json'

uri = URI('https://api.twitch.tv/kraken/streams')
response = Net::HTTP.get(uri)
streams = JSON.parse(response)["streams"]
streams.each do |stream|
    print '%-16.16s' % stream["channel"]["name"]
    print ' %-24.24s' % stream["game"]
    print ' %-9.9s' % stream["viewers"]
    print ' %-40.40s' % stream["channel"]["status"]
    puts
end
