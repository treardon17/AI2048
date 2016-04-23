from splinter import Browser
import os

browser = Browser('chrome')
currentFolderPath = os.path.dirname(os.path.abspath(__file__))
browser.visit("file:///"+currentFolderPath+"/2048-master/index.html")
print "executing keydown"

browser.execute_script("KeyboardInputManager.moveUp()")
browser.execute_script("KeyboardInputManager.moveLeft()")
browser.execute_script("KeyboardInputManager.moveRight()")
browser.execute_script("KeyboardInputManager.moveDown()")






"""browser.execute_script('\
    var e = new Event("keydown");\
    e.key="a";\
    e.keyCode=e.key.charCodeAt(37);\
    e.which=e.keyCode;\
    e.altKey=false;\
    e.ctrlKey=true;\
    e.shiftKey=false;\
    e.metaKey=false;\
    e.bubbles=true;\
    document.dispatchEvent(e);\
')"""

"""b.execute_script('var e = new Event("keydown"); e.key="a";e.keyCode=e.key.charCodeAt(37); e.which=e.keyCode; e.altKey=false; e.ctrlKey=true; e.shiftKey=false; e.metaKey=false; e.bubbles=true; document.dispatchEvent(e);')"""




















"""var keyboardEvent = document.createEvent("KeyboardEvent");
var initMethod = typeof keyboardEvent.initKeyboardEvent !== 'undefined' ? "initKeyboardEvent" : "initKeyEvent";


keyboardEvent[initMethod](
                   "keydown", // event type : keydown, keyup, keypress
                    true, // bubbles
                    true, // cancelable
                    window, // viewArg: should be window
                    false, // ctrlKeyArg
                    false, // altKeyArg
                    false, // shiftKeyArg
                    false, // metaKeyArg
                    40, // keyCodeArg : unsigned long the virtual key code, else 0
                    0 // charCodeArgs : unsigned long the Unicode character associated with the depressed key, else 0
);
document.dispatchEvent(keyboardEvent);"""
