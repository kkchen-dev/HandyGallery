// ==UserScript==
// @name         EXDL
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Download & Download M5
// @author       K
// @match        https://target.website/g/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    // Your code here...
    let pageNumber = document.querySelector('.ptds > a').innerHTML;
    let elementA = document.createElement('a');
    elementA.setAttribute('href', '');
    elementA.setAttribute('download', pageNumber + '.html');
    elementA.setAttribute('style', 'font-size:12px;');
    elementA.innerHTML = ' -- Download -- ';
    document.querySelector('.gtb').insertBefore(elementA, document.querySelector('.gpc'));

    // Modulo5
    // let p1 = Math.ceil(pageNumber / 5);
    // let p2 = pageNumber % 5 + 1;
    // p2 = p2 ? p2 : 5;
    // let elementB = document.createElement('a');
    // elementB.setAttribute('href', '');
    // elementB.setAttribute('download', p1 + '-' + p2 + '.html');
    // elementB.setAttribute('style', 'font-size:12px;');
    // elementB.innerHTML = ' -- DownloadM5 -- ';
    // document.querySelector('.gtb').insertBefore(elementB, document.querySelector('.gpc'));

    // Spacing
    let space = document.createElement('p');
    document.querySelector('.gtb').insertBefore(space, document.querySelector('.gpc'));
})();