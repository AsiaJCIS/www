
//document.oncontextmenu = new Function('self.event.returnValue=false'); // Disable right click context
//document.onselectstart = new Function('return false');
//document.ondragstart = new Function('return false');

String.prototype.trim = function() {
    return this.replace(/(^\s*)|(\s*$)/g, "");
}
var SlideContext = function(_hashCode, _imageCount, _showPager, _interval) {
    var Owner = this;
    this.HashCode = _hashCode;
    this.ImageCount = _imageCount;
    this.ImageIndex = 0;
    this.ShowPager = (_showPager == "True" || _showPager == true);
    this.Interval = _interval * 1000;
    this.Timer = null;

    this.$ = function(childID) {
        return document.getElementById(childID + "_" + this.HashCode);
    }
    this.SetImageByID = function(imageIndex) {
        if (this.ShowPager == true) {
            for (var i = 0; i < this.ImageCount; i++)
                this.$("pgr" + i).className = "pager1";
            this.$("pgr" + imageIndex).className = "pager2";
        }
        this.$("imgL").src = this.$("img" + imageIndex).src;
        this.$("imgL").alt = this.$("img" + imageIndex).alt;
        if (this.$("img" + imageIndex).title.length > 0)
            this.$("imgL").parentNode.href = this.$("img" + imageIndex).title;
        else
            this.$("imgL").parentNode.removeAttribute("href");
    }
    this.RotateImage = function() {
        this.ImageIndex++;
        if (this.ImageIndex >= this.ImageCount)
            this.ImageIndex = 0;
        this.SetImageByID(this.ImageIndex);
    }
    this.FreezeImage = function(imageIndex) {
        this.ImageIndex = imageIndex;
        this.SetImageByID(imageIndex);
        clearInterval(this.Timer);
    }
    this.StartSlide = function() {
        if (this.ImageCount > 1)
            this.Timer = setInterval(function() { Owner.RotateImage(); }, this.Interval);
    }
    this.Init = function() {
        if (this.ShowPager) {
            for (var i = 0; i < this.ImageCount; i++) {
                this.$("pgr" + i).p = i;
                this.$("pgr" + i).onmouseover = function() {
                    Owner.FreezeImage(this.p);
                }
                this.$("pgr" + i).onmouseout = function() {
                    Owner.StartSlide();
                }
            }
        }
        if (this.ImageCount > 0) {
            this.SetImageByID(0);
            this.StartSlide();
        }
    }
}

var MarqueeContext = function(_hashCode, _direction, _padding, _interval) {
    var Owner = this;
    this.HashCode = _hashCode;
    this.Direction = 0;
    this.Padding = _padding;
    this.Interval = _interval;
    this.Timer = null;

    this.$ = function(childID) {
        return document.getElementById(childID + "_" + this.HashCode);
    }
    this.Scroll = function(xOffset, yOffset) {
        var mqbox = this.$("mqbox");
        var x = mqbox.scrollLeft + xOffset, y = mqbox.scrollTop + yOffset;
        var cx = (mqbox.scrollWidth - this.Padding) / 2, cy = mqbox.scrollHeight / 2 - this.Padding;
        if (y >= cy)
            y -= cy;
        else if (y < 0)
            y += cy;
        if (x >= cx)
            x -= cx;
        else if (x < 0)
            x += cx;
        mqbox.scrollTop = y;
        mqbox.scrollLeft = x;
    }
    this.PauseScroll = function() {
        clearInterval(this.Timer);
    }
    this.StartScroll = function() {
        switch (this.Direction) {
            case 1: this.Timer = setInterval(function() { Owner.Scroll(1, 0) }, this.Interval); break;
            case 2: this.Timer = setInterval(function() { Owner.Scroll(0, 1) }, this.Interval); break;
            case 3: this.Timer = setInterval(function() { Owner.Scroll(-1, 0) }, this.Interval); break;
            case 4: this.Timer = setInterval(function() { Owner.Scroll(0, -1) }, this.Interval); break;
        }
    }
    this.Init = function() {
        switch (_direction.toString().toUpperCase()) {
            case "LEFT": case "L": case "1": this.Direction = 1; break;
            case "UP": case "U": case "2": this.Direction = 2; break;
            case "RIGHT": case "R": case "3": this.Direction = 3; break;
            case "DOWN": case "D": case "4": this.Direction = 4; break;
            default: return;
        }
        var mqbox = this.$("mqbox");
        if (this.Direction == 1 || this.Direction == 3) {
            var inner = document.createElement("div");
            inner.style.position = "absolute";
            inner.innerHTML = mqbox.innerHTML + "&nbsp;&nbsp;&nbsp;";
            inner.innerHTML += inner.innerHTML;
            mqbox.replaceChild(inner, mqbox.firstChild);
        }
        if (this.Direction == 2 || this.Direction == 4) {
            mqbox.innerHTML += "<br /><br />";
            mqbox.innerHTML += mqbox.innerHTML;
            mqbox.style.height = "30px";
        }
        mqbox.onmouseover = function() {
            Owner.PauseScroll();
        }
        mqbox.onmouseout = function() {
            Owner.StartScroll();
        }
        this.StartScroll();
    }
}

function flipto(tab1, tab2, tab3) {
    document.getElementById(tab1).style.display = '';
    document.getElementById(tab2).style.display = 'none';
    document.getElementById(tab3).style.display = 'none';
}
function stayleftbottom(box) {
    box.style.left = 0;
    box.style.top = document.documentElement.scrollTop + document.documentElement.clientHeight - box.scrollHeight;
}
function stayrightbottom(box) {
    box.style.right = 0;
    box.style.top = document.documentElement.scrollTop + document.documentElement.clientHeight - box.scrollHeight;
}
function setdropdownmenu(menubar) {
    for (i = 0; i < menubar.childNodes.length; i++) {
        node = menubar.childNodes[i];
        if (node.nodeName == "LI") {
            node.onmouseover = function() { this.className += " over"; }
            node.onmouseout = function() { this.className = this.className.replace(" over", ""); }
        }
    }
}
function writeflash(url, width, height) {
    if (url == null || url == '')
        return;
    document.write('<object type="application/x-shockwave-flash" data="' + url + '" width="' + width + '" height="' + height + '">');
    document.write('<param name="movie" value="' + url + '" />');
    document.write('<param name="quality" value="high" />');
    document.write('<param name="wmode" value="transparent" />');
    document.write('</object>');
}