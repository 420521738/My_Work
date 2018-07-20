#!/usr/bin/ruby
require 'digest'

def get_token(username,passwd)
    md5 = Digest::MD5.new
    time_stamp= Time.now.to_i
    md5.update "#{username}|#{passwd}|#{time_stamp}"
    #puts "#{username}  #{md5} --- #{time_stamp}"
    return [md5.hexdigest,time_stamp]
end

res = get_token 'user', 'AutoCmdb!23'

print  '--->', res 
