#!/usr/bin/ruby

# Lists accumulated email addresses in a copy-and-paste-able plaintext format

require 'cgi'
require 'json'
require 'mysql2'

cgi = CGI.new("html4")

def fatalerror(cgi, title, exception)
    return "#{title}: #{exception.message}"
end

cgi.out("text/plain") {

    begin
        configFile = json = File.read('../conf/config.json')
        config = JSON.parse(json)
    rescue Exception => e
        next fatalerror(cgi, "Configuration error", e)
    end

    begin

        body = ""

        client = Mysql2::Client.new(:host => config['host'], :username => config['username'],
            :password => config['password'], :database => config['db'])
        results = client.query("SELECT * FROM email order by name")

        if (results.count > 0)
            body += results.map { |result|
                result["name"] + " <" + result["email"] + ">"
            }.join(", ")
        end

        next body

    rescue Exception => e
        next fatalerror(cgi, "Something went wrong", e)
    end
}
