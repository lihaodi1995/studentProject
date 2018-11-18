function createXMLDOM(){
    var xmlDOM;
    if (window.ActiveXObject){
        xmlDOM = new ActiveXObject('Microsoft.XMLDOM');
    } 
    else if (document.implementation && document.implementation.createDocument){
        xmlDOM = document.implementation.createDocument('', '', null);
    }
    else{
        alert("您的浏览器不支持文档对象XMLDOM");
        return;
    }
    return xmlDOM;
}

function parserXMLToString(xmlDOM) {
    if (window.ActiveXObject){
        return xmlDOM.xml;
    }
    else if (document.implementation && document.implementation.createDocument){
        return new XMLSerializer().serializeToString(xmlDOM);
    }
}

function parserStringToXMLDOM(str){
    var parser = new DOMParser();
    var xmlDOM = parser.parseFromString(str, 'text/xml');
    return xmlDOM;
}