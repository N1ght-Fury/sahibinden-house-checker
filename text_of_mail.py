def html_text(house_link,title,price,m2,date,neighborhood,room,img):    
    
    text = """
    <!DOCTYPE html>
    <html>
    <body>
            
        <div style="width: 325px; border: 4px solid black; background-color: rgb(255, 255, 255);">
                
            <div style="border-bottom:3px solid black;">
                    <a href='https://www.sahibinden.com/'><img  style="display: block; margin-left: auto; margin-right: auto; vertical-align:middle; margin-top: 5px; margin-bottom: 5px;" src='http://www.aydoganlarotomotiv.com.tr/application/views/aydoganlar/layouts/images/sahibinden_logo.jpg' width="300px" height="60px"></a>
            </div>
                
            <div class="All Info" style="margin-top: 5px; text-decoration: none;">
                    
                <div class="Image Div">
                    <a href='""" + house_link + """'><img style="display: block; margin-left: auto; margin-right: auto; vertical-align:middle; margin-top: 5px;" src='""" + img + """' width="295px" height="250px"></a>
            
                    <div style="font: 18px/1.5 'Ubuntu', Arial, sans-serif;">
                        <a style="text-decoration: none;"><p style="background-color: rgb(25,25,25); margin-top: 6px; padding-left: 20px; color:white; font: 18px/1.5 'Ubuntu', Arial, sans-serif; margin-bottom: 6px;">""" + neighborhood + """</p></a>
                    </div>
            
                </div>
            
                <div class="Info Div">
            
                    <div style=" margin-left: 20px; width: 300px; font: 14px/1.5 'Ubuntu', Arial, sans-serif;">
                                
                            <span>
                                <span class="baslik">
                                    
                                    <span><b>Başlık: </b></span>   
                                    <span>""" + title + """</span>
                                    <br>
                                    
                                </span>

                                <span class="tarih" style="font: 26px;">
                                    
                                    <span><b>Tarih: </b></span>   
                                    <span>""" + date + """</span>
                                    <br>

                                </span>

                                <span class="fiyat">
                                    
                                    <span><b>Fiyat: </b></span>   
                                    <span>""" + price + """</span>
                                    <br>

                                </span>

                                <span class="alan">
                                    
                                    <span><b>m² (Brüt): </b></span>   
                                    <span>""" + m2 + """</span>
                                    <br>

                                </span>

                                <span class="oda">

                                    <span><b>Oda Sayısı: </b></span>   
                                    <span>""" + room + """</span>
                                    <br>

                                </span>

                                <div style="margin-bottom: 6px;"></div>
                            </span>
            
                    </div>
            
                </div>
            
            </div>
        </div>
            
    </body>
    </html>
    """
    
    return text