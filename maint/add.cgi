#!/usr/bin/ruby

# Shows count of collected addresses and the full list in readable format

require 'cgi'
require 'json'
require 'mysql2'

cgi = CGI.new("html4")

def failRequest(cgi, message)
    cgi.out("type" => "text/plain", "status" => "BAD_REQUEST") { message + "\n" }
    exit
end

def validateParams(cgi, name, email1, email2)
    failRequest(cgi, "MISSING:NAME") if name.nil? || name.empty?
    failRequest(cgi, "MISSING:EMAIL1") if email1.nil? || email1.empty?
    failRequest(cgi, "MISSING:EMAIL2") if email2.nil? || email2.empty?
end

def validateEmailMatches(cgi, email1, email2)
    failRequest(cgi, "EMAIL-MISMATCH") if email1 != email2
end

name = cgi.params["name"][0]
email1 = cgi.params["email1"][0]
email2 = cgi.params["email2"][0]

validateParams(cgi, name, email1, email2)
validateEmailMatches(cgi, email1, email2)

begin
    configFile = json = File.read('../conf/config.json')
    config = JSON.parse(json)
rescue Exception => e
    failRequest(cgi, "CONFIG-ERROR:#{e}")
end

begin
    client = Mysql2::Client.new(:host => config['host'], :username => config['username'],
        :password => config['password'], :database => config['db'])
    insert = client.prepare("INSERT INTO email (name, email) values(?, ?)")
    result = insert.execute(name, email1)
rescue Exception => e
    failRequest(cgi, "DB-ERROR:#{e}")
end

cgi.out("type" => "text/plain", "status" => "OK") { "OK" }
