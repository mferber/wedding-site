#!/usr/bin/ruby

# Shows count of collected addresses and the full list in readable format

require 'cgi'
require 'json'
require 'mysql2'

cgi = CGI.new("html4")

def fatalerror(cgi, title, exception)
    return cgi.h1 { CGI::escapeHTML(title) } + cgi.p { CGI::escapeHTML(exception.message) }
end

cgi.out {

    begin
        configFile = json = File.read('../conf/config.json')
        config = JSON.parse(json)
    rescue Exception => e
        next fatalerror(cgi, "Configuration error", e)
    end

    begin

        body = cgi.h1 { "Email subscriptions" }

        client = Mysql2::Client.new(:host => config['host'], :username => config['username'],
            :password => config['password'], :database => config['db'])
        results = client.query("SELECT * FROM email order by name")

        body += "You have #{results.count} email address#{results.count == 1 ? '' : 'es'} subscribed:"

        if (results.count > 0)
            body += cgi.ul {
                    results.map { |result|
                        cgi.li { result["name"] + " &mdash; " + result["email"] }
                    }.join('');
                } +
                cgi.div {
                    cgi.a({ :href=>'list.cgi' }) { "Copyable list" }
                }

        end

        next body

    rescue Exception => e
        next fatalerror(cgi, "Something went wrong", e)
    end
}
