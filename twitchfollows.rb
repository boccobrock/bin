#!/usr/bin/env ruby

require 'net/http'
require 'json'

uriuser = URI("https://api.twitch.tv/kraken/users/boccobrock/follows/channels")
responseuser = Net::HTTP.get(uriuser)
follows = JSON.parse(responseuser)["follows"]
channels = ''
follows.each do |stream|
    channels = channels + stream["channel"]["name"] + ','
end

uri = URI("https://api.twitch.tv/kraken/streams?channel=#{channels}")
response = Net::HTTP.get(uri)
streams = JSON.parse(response)["streams"]
streams.each do |stream|
    print '%-16.16s' % stream["channel"]["name"]
    print ' %-24.24s' % stream["game"]
    print ' %-9.9s' % stream["viewers"]
    print ' %-40.40s' % stream["channel"]["status"]
    puts
end
