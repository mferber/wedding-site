#!/usr/bin/env ruby
require "cgi"
require "json"
require "mysql2"

cgi = CGI.new("html3")
cgi.out("text/plain"){
	"Hello World #{Time.now}\n" + RUBY_VERSION
}

puts "\n"

begin
	configFile = json = File.read('../conf/config.json')
	config = JSON.parse(json)
rescue Exception => e
	puts "Configuration error: #{e}"
	return
end

puts "config: #{config}!\n"

begin
	client = Mysql2::Client.new(:host => config['host'], :username => config['username'],
		:password => config['password'], :database => config['db'])
	results = client.query("SELECT count(*) FROM email", :as => :array)
	puts "Count: #{results.first.first}\n"
rescue Exception => e
	puts "Error: #{e}\n\n"
end

puts "\nDone!\n\n"