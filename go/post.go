package main

import (
        "fmt"
        "net/http"
        "net/url"
        "bytes"
        "encoding/base64"
        "encoding/hex"
        "crypto/md5"
        "log"
        "os"
        "strings"
        "io/ioutil"
        "time"
)

func main(){
    dirpath, _ := os.Getwd()
    path := dirpath + "/small.jpg"

    fmt.Println("file: ", path)

    // platform api`
    req_url := "http://deepi.sogou.com/api/sogouService"

    // service
    svc := "translateOcr"
    //svc := "basicOpenOcr"

    pid := "your pid"
    secret_key := "your key"
    
    file, _ := ioutil.ReadFile(path)
    pic_buf := base64.StdEncoding.EncodeToString([]byte(file))

    nouce := "43"

    len := strings.Count(pic_buf, "") - 1
    log.Println("len: ", len)
    if len > 1024 {
        len = 1024
    }

    // calculate sign
    rq := ToString(pid, svc, nouce, pic_buf[:len], secret_key)
    md5ctx := md5.New()
    md5ctx.Write([]byte(rq))
    cipherStr := md5ctx.Sum(nil)
    sign := hex.EncodeToString(cipherStr)

    log.Println("sign: ", sign)

    extParams := map[string] string {
        "pid" : pid,
        "service": svc,
        "salt" : nouce,
        "nouce" : nouce,
        "from" : "en",
        "lang" : "en",
        "to" : "zh-CHS",
        //"result_type": "text",
        //"direction_detect":"false",
        "sign" : sign,
        "image" : pic_buf,
    }


    start := GetTime()
    request, err := Post(req_url, extParams)
    if err != nil {
        log.Fatal(err)
    }

    client := &http.Client{}
    res, err := client.Do(request)
    if err != nil {
        log.Fatal(err)
    } else {
        body := &bytes.Buffer{}
        _, err := body.ReadFrom(res.Body)
        if err != nil {
            log.Fatal(err)
        }
        res.Body.Close()
        //fmt.Println("status: ", res.Status, ", header: ", res.Header)
        fmt.Println(body)
    }
    
    end := GetTime()
    log.Println("cost: ", end - start)
}


func Post(req_url string, params map[string] string) (*http.Request, error){

    v := url.Values{}

    for key, val := range params {
        v.Set(key, val)
    }

    s := v.Encode() 

    req, err := http.NewRequest("POST", req_url, strings.NewReader(s))

    if err != nil {
        return nil, err
    }

    req.Header.Add("Content-Type", "application/x-www-form-urlencoded")

    return req, err
}


func ToString( strs ... string) string {
    var buf bytes.Buffer
    for _, value := range strs {
        buf.WriteString(value)
    }

    return buf.String()
}


func GetTime() uint64 {
    return uint64(time.Now().UnixNano() / 1e6)
}

        

