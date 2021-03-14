def uri_converter(uri):
    #print(uri) push to git

    for i in uri:
        if i.isalpha():
            #print(i, ord(i))
            sub = "{}".format(ord(i))
            uri = uri.replace(i, sub)

    #print(uri)
    return uri

uriExample = "2ekn2ttSfGqwhhate0LSR0"
print(uri_converter(uriExample))