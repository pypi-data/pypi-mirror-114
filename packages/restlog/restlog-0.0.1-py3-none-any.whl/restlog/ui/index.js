/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ([
/* 0 */,
/* 1 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Renderer": () => (/* binding */ Renderer),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var snabbdom_init__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(2);
/* harmony import */ var snabbdom_h__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(6);
/* harmony import */ var snabbdom_modules_class__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(7);
/* harmony import */ var snabbdom_modules_dataset__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(8);
/* harmony import */ var snabbdom_modules_eventlisteners__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(9);
/* harmony import */ var snabbdom_modules_style__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(10);
/* harmony import */ var _hat_core_util__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(11);
/** @module @hat-core/renderer
 */











// patched version of snabbdom's es/modules/attributes.js
const snabbdomAttributes = (() => {
    function updateAttrs(oldVnode, vnode) {
        var key, elm = vnode.elm, oldAttrs = oldVnode.data.attrs, attrs = vnode.data.attrs;
        if (!oldAttrs && !attrs)
            return;
        if (oldAttrs === attrs)
            return;
        oldAttrs = oldAttrs || {};
        attrs = attrs || {};
        for (key in attrs) {
            var cur = attrs[key];
            var old = oldAttrs[key];
            if (old !== cur) {
                if (cur === true) {
                    elm.setAttribute(key, "");
                }
                else if (cur === false) {
                    elm.removeAttribute(key);
                }
                else {
                    elm.setAttribute(key, cur);
                }
            }
        }
        for (key in oldAttrs) {
            if (!(key in attrs)) {
                elm.removeAttribute(key);
            }
        }
    }
    return { create: updateAttrs, update: updateAttrs };
})();


// patched version of snabbdom's es/modules/props.js
const snabbdomProps = (() => {
    function updateProps(oldVnode, vnode) {
        var key, cur, old, elm = vnode.elm, oldProps = oldVnode.data.props, props = vnode.data.props;
        if (!oldProps && !props)
            return;
        if (oldProps === props)
            return;
        oldProps = oldProps || {};
        props = props || {};
        for (key in oldProps) {
            if (!props[key]) {
                if (key === 'style') {
                    elm[key] = '';
                } else {
                    delete elm[key];
                }
            }
        }
        for (key in props) {
            cur = props[key];
            old = oldProps[key];
            if (old !== cur && (key !== 'value' || elm[key] !== cur)) {
                elm[key] = cur;
            }
        }
    }
    return { create: updateProps, update: updateProps };
})();


const patch = (0,snabbdom_init__WEBPACK_IMPORTED_MODULE_0__.init)([
    snabbdomAttributes,
    snabbdom_modules_class__WEBPACK_IMPORTED_MODULE_2__.classModule,
    snabbdom_modules_dataset__WEBPACK_IMPORTED_MODULE_3__.datasetModule,
    snabbdom_modules_eventlisteners__WEBPACK_IMPORTED_MODULE_4__.eventListenersModule,
    snabbdomProps,
    snabbdom_modules_style__WEBPACK_IMPORTED_MODULE_5__.styleModule
]);


function vhFromArray(node) {
    if (!node)
        return [];
    if (_hat_core_util__WEBPACK_IMPORTED_MODULE_6__.isString(node))
        return node;
    if (!_hat_core_util__WEBPACK_IMPORTED_MODULE_6__.isArray(node))
        throw 'Invalid node structure';
    if (node.length < 1)
        return [];
    if (typeof node[0] != 'string')
        return node.map(vhFromArray);
    const hasData = node.length > 1 && _hat_core_util__WEBPACK_IMPORTED_MODULE_6__.isObject(node[1]);
    const children = _hat_core_util__WEBPACK_IMPORTED_MODULE_6__.pipe(
        _hat_core_util__WEBPACK_IMPORTED_MODULE_6__.map(vhFromArray),
        _hat_core_util__WEBPACK_IMPORTED_MODULE_6__.flatten,
        Array.from
    )(node.slice(hasData ? 2 : 1));
    const result = hasData ?
        (0,snabbdom_h__WEBPACK_IMPORTED_MODULE_1__.h)(node[0], node[1], children) :
        (0,snabbdom_h__WEBPACK_IMPORTED_MODULE_1__.h)(node[0], children);
    return result;
}

/**
 * Virtual DOM renderer
 */
class Renderer extends EventTarget {

    /**
     * Calls `init` method
     * @param {HTMLElement} [el=document.body]
     * @param {Any} [initState=null]
     * @param {Function} [vtCb=null]
     * @param {Number} [maxFps=30]
     */
    constructor(el, initState, vtCb, maxFps) {
        super();
        this.init(el, initState, vtCb, maxFps);
    }

    /**
     * Initialize renderer
     * @param {HTMLElement} [el=document.body]
     * @param {Any} [initState=null]
     * @param {Function} [vtCb=null]
     * @param {Number} [maxFps=30]
     * @return {Promise}
     */
    init(el, initState, vtCb, maxFps) {
        this._state = null;
        this._changes = [];
        this._promise = null;
        this._timeout = null;
        this._lastRender = null;
        this._vtCb = vtCb;
        this._maxFps = _hat_core_util__WEBPACK_IMPORTED_MODULE_6__.isNumber(maxFps) ? maxFps : 30;
        this._vNode = el || document.querySelector('body');
        if (initState)
            return this.change(_ => initState);
        return new Promise(resolve => { resolve(); });
    }

    /**
      * Render
      */
    render() {
        if (!this._vtCb)
            return;
        this._lastRender = performance.now();
        const vNode = vhFromArray(this._vtCb(this));
        patch(this._vNode, vNode);
        this._vNode = vNode;
        this.dispatchEvent(new CustomEvent('render', {detail: this._state}));
    }

    /**
     * Get current state value referenced by `paths`
     * @param {...Path} paths
     * @return {Any}
     */
    get(...paths) {
        return _hat_core_util__WEBPACK_IMPORTED_MODULE_6__.get(paths, this._state);
    }

    /**
     * Change current state value referenced by `path`
     * @param {Path} path
     * @param {Any} value
     * @return {Promise}
     */
    set(path, value) {
        if (arguments.length < 2) {
            value = path;
            path = [];
        }
        return this.change(path, _ => value);
    }

    /**
     * Change current state value referenced by `path`
     * @param {Path} path
     * @param {Function} cb
     * @return {Promise}
     */
    change(path, cb) {
        if (arguments.length < 2) {
            cb = path;
            path = [];
        }
        this._changes.push([path, cb]);
        if (this._promise)
            return this._promise;
        this._promise = new Promise((resolve, reject) => {
            setTimeout(() => {
                try {
                    this._change();
                } catch(e) {
                    this._promise = null;
                    reject(e);
                    throw e;
                }
                this._promise = null;
                resolve();
            }, 0);
        });
        return this._promise;
    }

    _change() {
        let change = false;
        while (this._changes.length > 0) {
            const [path, cb] = this._changes.shift();
            const view = _hat_core_util__WEBPACK_IMPORTED_MODULE_6__.get(path);
            const oldState = this._state;
            this._state = _hat_core_util__WEBPACK_IMPORTED_MODULE_6__.change(path, cb, this._state);
            if (this._state && _hat_core_util__WEBPACK_IMPORTED_MODULE_6__.equals(view(oldState),
                                        view(this._state)))
                continue;
            change = true;
            if (!this._vtCb || this._timeout)
                continue;
            const delay = (!this._lastRender || !this._maxFps ?
                0 :
                (1000 / this._maxFps) -
                (performance.now() - this._lastRender));
            this._timeout = setTimeout(() => {
                this._timeout = null;
                this.render();
            }, (delay > 0 ? delay : 0));
        }
        if (change)
            this.dispatchEvent(
                new CustomEvent('change', {detail: this._state}));
    }
}
// Renderer.prototype.set = u.curry(Renderer.prototype.set);
// Renderer.prototype.change = u.curry(Renderer.prototype.change);


/**
 * Default renderer
 * @static
 * @type {Renderer}
 */
const defaultRenderer = (() => {
    const r = (window && window.__hat_default_renderer) || new Renderer();
    if (window)
        window.__hat_default_renderer = r;
    return r;
})();
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (defaultRenderer);


/***/ }),
/* 2 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "init": () => (/* binding */ init)
/* harmony export */ });
/* harmony import */ var _vnode_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(3);
/* harmony import */ var _is_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4);
/* harmony import */ var _htmldomapi_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(5);



function isUndef(s) {
    return s === undefined;
}
function isDef(s) {
    return s !== undefined;
}
const emptyNode = (0,_vnode_js__WEBPACK_IMPORTED_MODULE_0__.vnode)('', {}, [], undefined, undefined);
function sameVnode(vnode1, vnode2) {
    return vnode1.key === vnode2.key && vnode1.sel === vnode2.sel;
}
function isVnode(vnode) {
    return vnode.sel !== undefined;
}
function createKeyToOldIdx(children, beginIdx, endIdx) {
    var _a;
    const map = {};
    for (let i = beginIdx; i <= endIdx; ++i) {
        const key = (_a = children[i]) === null || _a === void 0 ? void 0 : _a.key;
        if (key !== undefined) {
            map[key] = i;
        }
    }
    return map;
}
const hooks = ['create', 'update', 'remove', 'destroy', 'pre', 'post'];
function init(modules, domApi) {
    let i;
    let j;
    const cbs = {
        create: [],
        update: [],
        remove: [],
        destroy: [],
        pre: [],
        post: []
    };
    const api = domApi !== undefined ? domApi : _htmldomapi_js__WEBPACK_IMPORTED_MODULE_2__.htmlDomApi;
    for (i = 0; i < hooks.length; ++i) {
        cbs[hooks[i]] = [];
        for (j = 0; j < modules.length; ++j) {
            const hook = modules[j][hooks[i]];
            if (hook !== undefined) {
                cbs[hooks[i]].push(hook);
            }
        }
    }
    function emptyNodeAt(elm) {
        const id = elm.id ? '#' + elm.id : '';
        const c = elm.className ? '.' + elm.className.split(' ').join('.') : '';
        return (0,_vnode_js__WEBPACK_IMPORTED_MODULE_0__.vnode)(api.tagName(elm).toLowerCase() + id + c, {}, [], undefined, elm);
    }
    function createRmCb(childElm, listeners) {
        return function rmCb() {
            if (--listeners === 0) {
                const parent = api.parentNode(childElm);
                api.removeChild(parent, childElm);
            }
        };
    }
    function createElm(vnode, insertedVnodeQueue) {
        var _a, _b;
        let i;
        let data = vnode.data;
        if (data !== undefined) {
            const init = (_a = data.hook) === null || _a === void 0 ? void 0 : _a.init;
            if (isDef(init)) {
                init(vnode);
                data = vnode.data;
            }
        }
        const children = vnode.children;
        const sel = vnode.sel;
        if (sel === '!') {
            if (isUndef(vnode.text)) {
                vnode.text = '';
            }
            vnode.elm = api.createComment(vnode.text);
        }
        else if (sel !== undefined) {
            // Parse selector
            const hashIdx = sel.indexOf('#');
            const dotIdx = sel.indexOf('.', hashIdx);
            const hash = hashIdx > 0 ? hashIdx : sel.length;
            const dot = dotIdx > 0 ? dotIdx : sel.length;
            const tag = hashIdx !== -1 || dotIdx !== -1 ? sel.slice(0, Math.min(hash, dot)) : sel;
            const elm = vnode.elm = isDef(data) && isDef(i = data.ns)
                ? api.createElementNS(i, tag)
                : api.createElement(tag);
            if (hash < dot)
                elm.setAttribute('id', sel.slice(hash + 1, dot));
            if (dotIdx > 0)
                elm.setAttribute('class', sel.slice(dot + 1).replace(/\./g, ' '));
            for (i = 0; i < cbs.create.length; ++i)
                cbs.create[i](emptyNode, vnode);
            if (_is_js__WEBPACK_IMPORTED_MODULE_1__.array(children)) {
                for (i = 0; i < children.length; ++i) {
                    const ch = children[i];
                    if (ch != null) {
                        api.appendChild(elm, createElm(ch, insertedVnodeQueue));
                    }
                }
            }
            else if (_is_js__WEBPACK_IMPORTED_MODULE_1__.primitive(vnode.text)) {
                api.appendChild(elm, api.createTextNode(vnode.text));
            }
            const hook = vnode.data.hook;
            if (isDef(hook)) {
                (_b = hook.create) === null || _b === void 0 ? void 0 : _b.call(hook, emptyNode, vnode);
                if (hook.insert) {
                    insertedVnodeQueue.push(vnode);
                }
            }
        }
        else {
            vnode.elm = api.createTextNode(vnode.text);
        }
        return vnode.elm;
    }
    function addVnodes(parentElm, before, vnodes, startIdx, endIdx, insertedVnodeQueue) {
        for (; startIdx <= endIdx; ++startIdx) {
            const ch = vnodes[startIdx];
            if (ch != null) {
                api.insertBefore(parentElm, createElm(ch, insertedVnodeQueue), before);
            }
        }
    }
    function invokeDestroyHook(vnode) {
        var _a, _b;
        const data = vnode.data;
        if (data !== undefined) {
            (_b = (_a = data === null || data === void 0 ? void 0 : data.hook) === null || _a === void 0 ? void 0 : _a.destroy) === null || _b === void 0 ? void 0 : _b.call(_a, vnode);
            for (let i = 0; i < cbs.destroy.length; ++i)
                cbs.destroy[i](vnode);
            if (vnode.children !== undefined) {
                for (let j = 0; j < vnode.children.length; ++j) {
                    const child = vnode.children[j];
                    if (child != null && typeof child !== 'string') {
                        invokeDestroyHook(child);
                    }
                }
            }
        }
    }
    function removeVnodes(parentElm, vnodes, startIdx, endIdx) {
        var _a, _b;
        for (; startIdx <= endIdx; ++startIdx) {
            let listeners;
            let rm;
            const ch = vnodes[startIdx];
            if (ch != null) {
                if (isDef(ch.sel)) {
                    invokeDestroyHook(ch);
                    listeners = cbs.remove.length + 1;
                    rm = createRmCb(ch.elm, listeners);
                    for (let i = 0; i < cbs.remove.length; ++i)
                        cbs.remove[i](ch, rm);
                    const removeHook = (_b = (_a = ch === null || ch === void 0 ? void 0 : ch.data) === null || _a === void 0 ? void 0 : _a.hook) === null || _b === void 0 ? void 0 : _b.remove;
                    if (isDef(removeHook)) {
                        removeHook(ch, rm);
                    }
                    else {
                        rm();
                    }
                }
                else { // Text node
                    api.removeChild(parentElm, ch.elm);
                }
            }
        }
    }
    function updateChildren(parentElm, oldCh, newCh, insertedVnodeQueue) {
        let oldStartIdx = 0;
        let newStartIdx = 0;
        let oldEndIdx = oldCh.length - 1;
        let oldStartVnode = oldCh[0];
        let oldEndVnode = oldCh[oldEndIdx];
        let newEndIdx = newCh.length - 1;
        let newStartVnode = newCh[0];
        let newEndVnode = newCh[newEndIdx];
        let oldKeyToIdx;
        let idxInOld;
        let elmToMove;
        let before;
        while (oldStartIdx <= oldEndIdx && newStartIdx <= newEndIdx) {
            if (oldStartVnode == null) {
                oldStartVnode = oldCh[++oldStartIdx]; // Vnode might have been moved left
            }
            else if (oldEndVnode == null) {
                oldEndVnode = oldCh[--oldEndIdx];
            }
            else if (newStartVnode == null) {
                newStartVnode = newCh[++newStartIdx];
            }
            else if (newEndVnode == null) {
                newEndVnode = newCh[--newEndIdx];
            }
            else if (sameVnode(oldStartVnode, newStartVnode)) {
                patchVnode(oldStartVnode, newStartVnode, insertedVnodeQueue);
                oldStartVnode = oldCh[++oldStartIdx];
                newStartVnode = newCh[++newStartIdx];
            }
            else if (sameVnode(oldEndVnode, newEndVnode)) {
                patchVnode(oldEndVnode, newEndVnode, insertedVnodeQueue);
                oldEndVnode = oldCh[--oldEndIdx];
                newEndVnode = newCh[--newEndIdx];
            }
            else if (sameVnode(oldStartVnode, newEndVnode)) { // Vnode moved right
                patchVnode(oldStartVnode, newEndVnode, insertedVnodeQueue);
                api.insertBefore(parentElm, oldStartVnode.elm, api.nextSibling(oldEndVnode.elm));
                oldStartVnode = oldCh[++oldStartIdx];
                newEndVnode = newCh[--newEndIdx];
            }
            else if (sameVnode(oldEndVnode, newStartVnode)) { // Vnode moved left
                patchVnode(oldEndVnode, newStartVnode, insertedVnodeQueue);
                api.insertBefore(parentElm, oldEndVnode.elm, oldStartVnode.elm);
                oldEndVnode = oldCh[--oldEndIdx];
                newStartVnode = newCh[++newStartIdx];
            }
            else {
                if (oldKeyToIdx === undefined) {
                    oldKeyToIdx = createKeyToOldIdx(oldCh, oldStartIdx, oldEndIdx);
                }
                idxInOld = oldKeyToIdx[newStartVnode.key];
                if (isUndef(idxInOld)) { // New element
                    api.insertBefore(parentElm, createElm(newStartVnode, insertedVnodeQueue), oldStartVnode.elm);
                }
                else {
                    elmToMove = oldCh[idxInOld];
                    if (elmToMove.sel !== newStartVnode.sel) {
                        api.insertBefore(parentElm, createElm(newStartVnode, insertedVnodeQueue), oldStartVnode.elm);
                    }
                    else {
                        patchVnode(elmToMove, newStartVnode, insertedVnodeQueue);
                        oldCh[idxInOld] = undefined;
                        api.insertBefore(parentElm, elmToMove.elm, oldStartVnode.elm);
                    }
                }
                newStartVnode = newCh[++newStartIdx];
            }
        }
        if (oldStartIdx <= oldEndIdx || newStartIdx <= newEndIdx) {
            if (oldStartIdx > oldEndIdx) {
                before = newCh[newEndIdx + 1] == null ? null : newCh[newEndIdx + 1].elm;
                addVnodes(parentElm, before, newCh, newStartIdx, newEndIdx, insertedVnodeQueue);
            }
            else {
                removeVnodes(parentElm, oldCh, oldStartIdx, oldEndIdx);
            }
        }
    }
    function patchVnode(oldVnode, vnode, insertedVnodeQueue) {
        var _a, _b, _c, _d, _e;
        const hook = (_a = vnode.data) === null || _a === void 0 ? void 0 : _a.hook;
        (_b = hook === null || hook === void 0 ? void 0 : hook.prepatch) === null || _b === void 0 ? void 0 : _b.call(hook, oldVnode, vnode);
        const elm = vnode.elm = oldVnode.elm;
        const oldCh = oldVnode.children;
        const ch = vnode.children;
        if (oldVnode === vnode)
            return;
        if (vnode.data !== undefined) {
            for (let i = 0; i < cbs.update.length; ++i)
                cbs.update[i](oldVnode, vnode);
            (_d = (_c = vnode.data.hook) === null || _c === void 0 ? void 0 : _c.update) === null || _d === void 0 ? void 0 : _d.call(_c, oldVnode, vnode);
        }
        if (isUndef(vnode.text)) {
            if (isDef(oldCh) && isDef(ch)) {
                if (oldCh !== ch)
                    updateChildren(elm, oldCh, ch, insertedVnodeQueue);
            }
            else if (isDef(ch)) {
                if (isDef(oldVnode.text))
                    api.setTextContent(elm, '');
                addVnodes(elm, null, ch, 0, ch.length - 1, insertedVnodeQueue);
            }
            else if (isDef(oldCh)) {
                removeVnodes(elm, oldCh, 0, oldCh.length - 1);
            }
            else if (isDef(oldVnode.text)) {
                api.setTextContent(elm, '');
            }
        }
        else if (oldVnode.text !== vnode.text) {
            if (isDef(oldCh)) {
                removeVnodes(elm, oldCh, 0, oldCh.length - 1);
            }
            api.setTextContent(elm, vnode.text);
        }
        (_e = hook === null || hook === void 0 ? void 0 : hook.postpatch) === null || _e === void 0 ? void 0 : _e.call(hook, oldVnode, vnode);
    }
    return function patch(oldVnode, vnode) {
        let i, elm, parent;
        const insertedVnodeQueue = [];
        for (i = 0; i < cbs.pre.length; ++i)
            cbs.pre[i]();
        if (!isVnode(oldVnode)) {
            oldVnode = emptyNodeAt(oldVnode);
        }
        if (sameVnode(oldVnode, vnode)) {
            patchVnode(oldVnode, vnode, insertedVnodeQueue);
        }
        else {
            elm = oldVnode.elm;
            parent = api.parentNode(elm);
            createElm(vnode, insertedVnodeQueue);
            if (parent !== null) {
                api.insertBefore(parent, vnode.elm, api.nextSibling(elm));
                removeVnodes(parent, [oldVnode], 0, 0);
            }
        }
        for (i = 0; i < insertedVnodeQueue.length; ++i) {
            insertedVnodeQueue[i].data.hook.insert(insertedVnodeQueue[i]);
        }
        for (i = 0; i < cbs.post.length; ++i)
            cbs.post[i]();
        return vnode;
    };
}
//# sourceMappingURL=init.js.map

/***/ }),
/* 3 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "vnode": () => (/* binding */ vnode)
/* harmony export */ });
function vnode(sel, data, children, text, elm) {
    const key = data === undefined ? undefined : data.key;
    return { sel, data, children, text, elm, key };
}
//# sourceMappingURL=vnode.js.map

/***/ }),
/* 4 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "array": () => (/* binding */ array),
/* harmony export */   "primitive": () => (/* binding */ primitive)
/* harmony export */ });
const array = Array.isArray;
function primitive(s) {
    return typeof s === 'string' || typeof s === 'number';
}
//# sourceMappingURL=is.js.map

/***/ }),
/* 5 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "htmlDomApi": () => (/* binding */ htmlDomApi)
/* harmony export */ });
function createElement(tagName) {
    return document.createElement(tagName);
}
function createElementNS(namespaceURI, qualifiedName) {
    return document.createElementNS(namespaceURI, qualifiedName);
}
function createTextNode(text) {
    return document.createTextNode(text);
}
function createComment(text) {
    return document.createComment(text);
}
function insertBefore(parentNode, newNode, referenceNode) {
    parentNode.insertBefore(newNode, referenceNode);
}
function removeChild(node, child) {
    node.removeChild(child);
}
function appendChild(node, child) {
    node.appendChild(child);
}
function parentNode(node) {
    return node.parentNode;
}
function nextSibling(node) {
    return node.nextSibling;
}
function tagName(elm) {
    return elm.tagName;
}
function setTextContent(node, text) {
    node.textContent = text;
}
function getTextContent(node) {
    return node.textContent;
}
function isElement(node) {
    return node.nodeType === 1;
}
function isText(node) {
    return node.nodeType === 3;
}
function isComment(node) {
    return node.nodeType === 8;
}
const htmlDomApi = {
    createElement,
    createElementNS,
    createTextNode,
    createComment,
    insertBefore,
    removeChild,
    appendChild,
    parentNode,
    nextSibling,
    tagName,
    setTextContent,
    getTextContent,
    isElement,
    isText,
    isComment,
};
//# sourceMappingURL=htmldomapi.js.map

/***/ }),
/* 6 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "h": () => (/* binding */ h)
/* harmony export */ });
/* harmony import */ var _vnode_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(3);
/* harmony import */ var _is_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4);


function addNS(data, children, sel) {
    data.ns = 'http://www.w3.org/2000/svg';
    if (sel !== 'foreignObject' && children !== undefined) {
        for (let i = 0; i < children.length; ++i) {
            const childData = children[i].data;
            if (childData !== undefined) {
                addNS(childData, children[i].children, children[i].sel);
            }
        }
    }
}
function h(sel, b, c) {
    var data = {};
    var children;
    var text;
    var i;
    if (c !== undefined) {
        if (b !== null) {
            data = b;
        }
        if (_is_js__WEBPACK_IMPORTED_MODULE_1__.array(c)) {
            children = c;
        }
        else if (_is_js__WEBPACK_IMPORTED_MODULE_1__.primitive(c)) {
            text = c;
        }
        else if (c && c.sel) {
            children = [c];
        }
    }
    else if (b !== undefined && b !== null) {
        if (_is_js__WEBPACK_IMPORTED_MODULE_1__.array(b)) {
            children = b;
        }
        else if (_is_js__WEBPACK_IMPORTED_MODULE_1__.primitive(b)) {
            text = b;
        }
        else if (b && b.sel) {
            children = [b];
        }
        else {
            data = b;
        }
    }
    if (children !== undefined) {
        for (i = 0; i < children.length; ++i) {
            if (_is_js__WEBPACK_IMPORTED_MODULE_1__.primitive(children[i]))
                children[i] = (0,_vnode_js__WEBPACK_IMPORTED_MODULE_0__.vnode)(undefined, undefined, undefined, children[i], undefined);
        }
    }
    if (sel[0] === 's' && sel[1] === 'v' && sel[2] === 'g' &&
        (sel.length === 3 || sel[3] === '.' || sel[3] === '#')) {
        addNS(data, children, sel);
    }
    return (0,_vnode_js__WEBPACK_IMPORTED_MODULE_0__.vnode)(sel, data, children, text, undefined);
}
;
//# sourceMappingURL=h.js.map

/***/ }),
/* 7 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "classModule": () => (/* binding */ classModule)
/* harmony export */ });
function updateClass(oldVnode, vnode) {
    var cur;
    var name;
    var elm = vnode.elm;
    var oldClass = oldVnode.data.class;
    var klass = vnode.data.class;
    if (!oldClass && !klass)
        return;
    if (oldClass === klass)
        return;
    oldClass = oldClass || {};
    klass = klass || {};
    for (name in oldClass) {
        if (oldClass[name] &&
            !Object.prototype.hasOwnProperty.call(klass, name)) {
            // was `true` and now not provided
            elm.classList.remove(name);
        }
    }
    for (name in klass) {
        cur = klass[name];
        if (cur !== oldClass[name]) {
            elm.classList[cur ? 'add' : 'remove'](name);
        }
    }
}
const classModule = { create: updateClass, update: updateClass };
//# sourceMappingURL=class.js.map

/***/ }),
/* 8 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "datasetModule": () => (/* binding */ datasetModule)
/* harmony export */ });
const CAPS_REGEX = /[A-Z]/g;
function updateDataset(oldVnode, vnode) {
    const elm = vnode.elm;
    let oldDataset = oldVnode.data.dataset;
    let dataset = vnode.data.dataset;
    let key;
    if (!oldDataset && !dataset)
        return;
    if (oldDataset === dataset)
        return;
    oldDataset = oldDataset || {};
    dataset = dataset || {};
    const d = elm.dataset;
    for (key in oldDataset) {
        if (!dataset[key]) {
            if (d) {
                if (key in d) {
                    delete d[key];
                }
            }
            else {
                elm.removeAttribute('data-' + key.replace(CAPS_REGEX, '-$&').toLowerCase());
            }
        }
    }
    for (key in dataset) {
        if (oldDataset[key] !== dataset[key]) {
            if (d) {
                d[key] = dataset[key];
            }
            else {
                elm.setAttribute('data-' + key.replace(CAPS_REGEX, '-$&').toLowerCase(), dataset[key]);
            }
        }
    }
}
const datasetModule = { create: updateDataset, update: updateDataset };
//# sourceMappingURL=dataset.js.map

/***/ }),
/* 9 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "eventListenersModule": () => (/* binding */ eventListenersModule)
/* harmony export */ });
function invokeHandler(handler, vnode, event) {
    if (typeof handler === 'function') {
        // call function handler
        handler.call(vnode, event, vnode);
    }
    else if (typeof handler === 'object') {
        // call multiple handlers
        for (var i = 0; i < handler.length; i++) {
            invokeHandler(handler[i], vnode, event);
        }
    }
}
function handleEvent(event, vnode) {
    var name = event.type;
    var on = vnode.data.on;
    // call event handler(s) if exists
    if (on && on[name]) {
        invokeHandler(on[name], vnode, event);
    }
}
function createListener() {
    return function handler(event) {
        handleEvent(event, handler.vnode);
    };
}
function updateEventListeners(oldVnode, vnode) {
    var oldOn = oldVnode.data.on;
    var oldListener = oldVnode.listener;
    var oldElm = oldVnode.elm;
    var on = vnode && vnode.data.on;
    var elm = (vnode && vnode.elm);
    var name;
    // optimization for reused immutable handlers
    if (oldOn === on) {
        return;
    }
    // remove existing listeners which no longer used
    if (oldOn && oldListener) {
        // if element changed or deleted we remove all existing listeners unconditionally
        if (!on) {
            for (name in oldOn) {
                // remove listener if element was changed or existing listeners removed
                oldElm.removeEventListener(name, oldListener, false);
            }
        }
        else {
            for (name in oldOn) {
                // remove listener if existing listener removed
                if (!on[name]) {
                    oldElm.removeEventListener(name, oldListener, false);
                }
            }
        }
    }
    // add new listeners which has not already attached
    if (on) {
        // reuse existing listener or create new
        var listener = vnode.listener = oldVnode.listener || createListener();
        // update vnode for listener
        listener.vnode = vnode;
        // if element changed or added we add all needed listeners unconditionally
        if (!oldOn) {
            for (name in on) {
                // add listener if element was changed or new listeners added
                elm.addEventListener(name, listener, false);
            }
        }
        else {
            for (name in on) {
                // add listener if new listener added
                if (!oldOn[name]) {
                    elm.addEventListener(name, listener, false);
                }
            }
        }
    }
}
const eventListenersModule = {
    create: updateEventListeners,
    update: updateEventListeners,
    destroy: updateEventListeners
};
//# sourceMappingURL=eventlisteners.js.map

/***/ }),
/* 10 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "styleModule": () => (/* binding */ styleModule)
/* harmony export */ });
// Bindig `requestAnimationFrame` like this fixes a bug in IE/Edge. See #360 and #409.
var raf = (typeof window !== 'undefined' && (window.requestAnimationFrame).bind(window)) || setTimeout;
var nextFrame = function (fn) {
    raf(function () {
        raf(fn);
    });
};
var reflowForced = false;
function setNextFrame(obj, prop, val) {
    nextFrame(function () {
        obj[prop] = val;
    });
}
function updateStyle(oldVnode, vnode) {
    var cur;
    var name;
    var elm = vnode.elm;
    var oldStyle = oldVnode.data.style;
    var style = vnode.data.style;
    if (!oldStyle && !style)
        return;
    if (oldStyle === style)
        return;
    oldStyle = oldStyle || {};
    style = style || {};
    var oldHasDel = 'delayed' in oldStyle;
    for (name in oldStyle) {
        if (!style[name]) {
            if (name[0] === '-' && name[1] === '-') {
                elm.style.removeProperty(name);
            }
            else {
                elm.style[name] = '';
            }
        }
    }
    for (name in style) {
        cur = style[name];
        if (name === 'delayed' && style.delayed) {
            for (const name2 in style.delayed) {
                cur = style.delayed[name2];
                if (!oldHasDel || cur !== oldStyle.delayed[name2]) {
                    setNextFrame(elm.style, name2, cur);
                }
            }
        }
        else if (name !== 'remove' && cur !== oldStyle[name]) {
            if (name[0] === '-' && name[1] === '-') {
                elm.style.setProperty(name, cur);
            }
            else {
                elm.style[name] = cur;
            }
        }
    }
}
function applyDestroyStyle(vnode) {
    var style;
    var name;
    var elm = vnode.elm;
    var s = vnode.data.style;
    if (!s || !(style = s.destroy))
        return;
    for (name in style) {
        elm.style[name] = style[name];
    }
}
function applyRemoveStyle(vnode, rm) {
    var s = vnode.data.style;
    if (!s || !s.remove) {
        rm();
        return;
    }
    if (!reflowForced) {
        // eslint-disable-next-line @typescript-eslint/no-unused-expressions
        vnode.elm.offsetLeft;
        reflowForced = true;
    }
    var name;
    var elm = vnode.elm;
    var i = 0;
    var compStyle;
    var style = s.remove;
    var amount = 0;
    var applied = [];
    for (name in style) {
        applied.push(name);
        elm.style[name] = style[name];
    }
    compStyle = getComputedStyle(elm);
    var props = compStyle['transition-property'].split(', ');
    for (; i < props.length; ++i) {
        if (applied.indexOf(props[i]) !== -1)
            amount++;
    }
    elm.addEventListener('transitionend', function (ev) {
        if (ev.target === elm)
            --amount;
        if (amount === 0)
            rm();
    });
}
function forceReflow() {
    reflowForced = false;
}
const styleModule = {
    pre: forceReflow,
    create: updateStyle,
    update: updateStyle,
    destroy: applyDestroyStyle,
    remove: applyRemoveStyle
};
//# sourceMappingURL=style.js.map

/***/ }),
/* 11 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "identity": () => (/* binding */ identity),
/* harmony export */   "isNil": () => (/* binding */ isNil),
/* harmony export */   "isBoolean": () => (/* binding */ isBoolean),
/* harmony export */   "isInteger": () => (/* binding */ isInteger),
/* harmony export */   "isNumber": () => (/* binding */ isNumber),
/* harmony export */   "isString": () => (/* binding */ isString),
/* harmony export */   "isArray": () => (/* binding */ isArray),
/* harmony export */   "isObject": () => (/* binding */ isObject),
/* harmony export */   "strictParseInt": () => (/* binding */ strictParseInt),
/* harmony export */   "strictParseFloat": () => (/* binding */ strictParseFloat),
/* harmony export */   "clone": () => (/* binding */ clone),
/* harmony export */   "zip": () => (/* binding */ zip),
/* harmony export */   "toPairs": () => (/* binding */ toPairs),
/* harmony export */   "fromPairs": () => (/* binding */ fromPairs),
/* harmony export */   "flatten": () => (/* binding */ flatten),
/* harmony export */   "pipe": () => (/* binding */ pipe),
/* harmony export */   "flap": () => (/* binding */ flap),
/* harmony export */   "curry": () => (/* binding */ curry),
/* harmony export */   "equals": () => (/* binding */ equals),
/* harmony export */   "repeat": () => (/* binding */ repeat),
/* harmony export */   "get": () => (/* binding */ get),
/* harmony export */   "change": () => (/* binding */ change),
/* harmony export */   "set": () => (/* binding */ set),
/* harmony export */   "omit": () => (/* binding */ omit),
/* harmony export */   "move": () => (/* binding */ move),
/* harmony export */   "sort": () => (/* binding */ sort),
/* harmony export */   "sortBy": () => (/* binding */ sortBy),
/* harmony export */   "pick": () => (/* binding */ pick),
/* harmony export */   "map": () => (/* binding */ map),
/* harmony export */   "filter": () => (/* binding */ filter),
/* harmony export */   "append": () => (/* binding */ append),
/* harmony export */   "reduce": () => (/* binding */ reduce),
/* harmony export */   "merge": () => (/* binding */ merge),
/* harmony export */   "mergeAll": () => (/* binding */ mergeAll),
/* harmony export */   "find": () => (/* binding */ find),
/* harmony export */   "findIndex": () => (/* binding */ findIndex),
/* harmony export */   "concat": () => (/* binding */ concat),
/* harmony export */   "union": () => (/* binding */ union),
/* harmony export */   "contains": () => (/* binding */ contains),
/* harmony export */   "insert": () => (/* binding */ insert),
/* harmony export */   "slice": () => (/* binding */ slice),
/* harmony export */   "reverse": () => (/* binding */ reverse),
/* harmony export */   "length": () => (/* binding */ length),
/* harmony export */   "inc": () => (/* binding */ inc),
/* harmony export */   "dec": () => (/* binding */ dec),
/* harmony export */   "not": () => (/* binding */ not),
/* harmony export */   "sleep": () => (/* binding */ sleep),
/* harmony export */   "delay": () => (/* binding */ delay)
/* harmony export */ });
/**
 * Utility library for manipulation of JSON data.
 *
 * Main characteristics:
 *   - input/output data types are limited to JSON data, functions and
 *     `undefined` (sparse arrays and complex objects with prototype chain are
 *     not supported)
 *   - functional API with curried functions (similar to ramdajs)
 *   - implementation based on natively supported browser JS API
 *   - scope limited to most used functions in hat projects
 *   - usage of `paths` instead of `lenses`
 *
 * TODO: define convetion for naming arguments based on their type and
 *       semantics
 *
 * @module @hat-core/util
 */

/**
 * Path can be an object property name, array index, or array of Paths
 *
 * TODO: explain paths and path compositions (include examples)
 *
 * @typedef {(String|Number|Path[])} module:@hat-core/util.Path
 */

/**
 * Identity function returning same value provided as argument.
 *
 * @function
 * @sig a -> a
 * @param {*} x input value
 * @return {*} same value as input
 */
const identity = x => x;

/**
 * Check if value is `null` or `undefined`.
 *
 * For same argument, if this function returns `true`, functions `isBoolean`,
 * `isInteger`, `isNumber`, `isString`, `isArray` and `isObject` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isNil = x => x == null;

/**
 * Check if value is Boolean.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isInteger`, `isNumber`, `isString`, `isArray` and `isObject` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isBoolean = x => typeof(x) == 'boolean';

/**
 * Check if value is Integer.
 *
 * For same argument, if this function returns `true`, function `isNumber` will
 * also return `true`.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isString`, `isArray` and `isObject` will return `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @type {Boolean}
 */
const isInteger = Number.isInteger;

/**
 * Check if value is Number.
 *
 * For same argument, if this function returns `true`, function `isInteger` may
 * also return `true` if argument is integer number.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isString`, `isArray` and `isObject` will return `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isNumber = x => typeof(x) == 'number';

/**
 * Check if value is String.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isInteger`, `isNumber`, `isArray`, and `isObject` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {Any} x input value
 * @type {Boolean}
 */
const isString = x => typeof(x) == 'string';

/**
 * Check if value is Array.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isInteger`, `isNumber`, `isString`, and `isObject` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isArray = Array.isArray;

/**
 * Check if value is Object.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isInteger`, `isNumber`, `isString`, and `isArray` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isObject = x => typeof(x) == 'object' &&
                             !isArray(x) &&
                             !isNil(x);

/**
 * Strictly parse integer from string
 *
 * If provided string doesn't represent integer value, `NaN` is returned.
 *
 * @function
 * @sig String -> Number
 * @param {String} value
 * @return {Number}
 */
function strictParseInt(value) {
    if (/^(-|\+)?([0-9]+)$/.test(value))
        return Number(value);
    return NaN;
}

/**
 * Strictly parse floating point number from string
 *
 * If provided string doesn't represent valid number, `NaN` is returned.
 *
 * @function
 * @sig String -> Number
 * @param {String} value
 * @return {Number}
 */
function strictParseFloat(value) {
    if (/^(-|\+)?([0-9]+(\.[0-9]+)?)$/.test(value))
        return Number(value);
    return NaN;
}

/**
 * Create new deep copy of input value.
 *
 * In case of Objects or Arrays, new instances are created with elements
 * obtained by recursivly calling `clone` in input argument values.
 *
 * @function
 * @sig * -> *
 * @param {*} x value
 * @return {*} copy of value
 */
function clone(x) {
    if (isArray(x))
        return Array.from(x, clone);
    if (isObject(x)) {
        let ret = {};
        for (let i in x)
            ret[i] = clone(x[i]);
        return ret;
    }
    return x;
}

/**
 * Combine two arrays in single array of pairs
 *
 * The returned array is truncated to the length of the shorter of the two
 * input arrays.
 *
 * @function
 * @sig [a] -> [b] -> [[a,b]]
 * @param {Array} arr1
 * @param {Array} arr2
 * @return {Array}
 */
function zip(arr1, arr2) {
    return Array.from((function*() {
        for (let i = 0; i < arr1.length || i < arr2.length; ++i)
            yield [arr1[i], arr2[i]];
    })());
}

/**
 * Convert object to array of key, value pairs
 *
 * @function
 * @sig Object -> [[String,*]]
 * @param {Object} obj
 * @return {Array}
 */
function toPairs(obj) {
    return Object.entries(obj);
}

/**
 * Convert array of key, value pairs to object
 *
 * @function
 * @sig [[String,*]] -> Object
 * @param {Array} arr
 * @return {Object}
 */
function fromPairs(arr) {
    let ret = {};
    for (let [k, v] of arr)
        ret[k] = v;
    return ret;
}

/**
 * Flatten nested arrays.
 *
 * Create array with same elements as in input array where all elements which
 * are also arrays are replaced with elements of resulting recursive
 * application of flatten function.
 *
 * If argument is not an array, function returns the argument encapsulated in
 * an array.
 *
 * @function
 * @sig [a] -> [b]
 * @param {*} arr
 * @return {Array}
 */
function flatten(arr) {
    return isArray(arr) ? arr.flat(Infinity) : [arr];
}

/**
 * Pipe function calls
 *
 * Pipe provides functional composition with reversed order. First function
 * may have any arity and all other functions are called with only single
 * argument (result from previous function application).
 *
 * In case when no function is provided, pipe returns identity function.
 *
 * @function
 * @sig (((a1, a2, ..., an) -> b1), (b1 -> b2), ..., (bm1 -> bm)) -> ((a1, a2, ..., an) -> bm)
 * @param {...Function} fns functions
 * @return {Function}
 */
function pipe(...fns) {
    if (fns.length < 1)
        return identity;
    return function (...args) {
        let ret = fns[0].apply(this, args);
        for (let fn of fns.slice(1))
            ret = fn(ret);
        return ret;
    };
}

/**
 * Apply list of functions to same arguments and return list of results
 *
 * @function
 * @sig ((a1 -> ... -> an -> b1), ..., (a1 -> ... -> an -> bm)) -> (a1 -> ... -> an -> [b1,...,bm])
 * @param {...Function} fns functions
 * @return {Function}
 */
function flap(...fns) {
    return (...args) => fns.map(fn => fn.apply(this, args));
}

/**
 * Curry function with fixed arguments lenth
 *
 * Function arity is determined based on function's length property.
 *
 * @function
 * @sig (* -> a) -> (* -> a)
 * @param {Function} fn
 * @return {Function}
 */
function curry(fn) {
    let wrapper = function(oldArgs) {
        return function(...args) {
            args = oldArgs.concat(args);
            if (args.length >= fn.length)
                return fn(...args);
            return wrapper(args);
        };
    };
    return wrapper([]);
}

/**
 * Deep object equality
 * (curried function)
 *
 * @function
 * @sig a -> b -> Boolean
 * @param {*} x
 * @param {*} y
 * @return {Boolean}
 */
const equals = curry((x, y) => {
    if (x === y)
        return true;
    if (typeof(x) != 'object' ||
        typeof(y) != 'object' ||
        x === null ||
        y === null)
        return false;
    if (Array.isArray(x) && Array.isArray(y)) {
        if (x.length != y.length)
            return false;
        for (let [a, b] of zip(x, y)) {
            if (!equals(a, b))
                return false;
        }
        return true;
    } else if (!Array.isArray(x) && !Array.isArray(y)) {
        if (Object.keys(x).length != Object.keys(y).length)
            return false;
        for (let key in x) {
            if (!(key in y))
                return false;
        }
        for (let key in x) {
            if (!equals(x[key], y[key]))
                return false;
        }
        return true;
    }
    return false;
});


/**
 * Create array by repeating same value
 * (curried function)
 *
 * @function
 * @sig a -> Number -> [a]
 * @param {*} x
 * @param {Number} n
 * @return {Array}
 */
const repeat = curry((x, n) => Array.from({length: n}, _ => x));

/**
 * Get value referenced by path
 * (curried function)
 *
 * If input value doesn't contain provided path value, `undefined` is returned.
 *
 * @function
 * @sig Path -> a -> b
 * @param {Path} path
 * @param {*} x
 * @return {*}
 */
const get = curry((path, x) => {
    let ret = x;
    for (let i of flatten(path)) {
        if (ret === null || typeof(ret) != 'object')
            return undefined;
        ret = ret[i];
    }
    return ret;
});

/**
 * Change value referenced with path by appling function
 * (curried function)
 *
 * @function
 * @sig Path -> (a -> b) -> c -> c
 * @param {Path} path
 * @param {Function} fn
 * @param {*} x
 * @return {*}
 */
const change = curry((path, fn, x) => {
    return (function change(path, x) {
        if (path.length < 1)
            return fn(x);
        const [first, ...rest] = path;
        if (isInteger(first)) {
            x = (isArray(x) ? Array.from(x) : repeat(undefined, first));
        } else if (isString(first)) {
            x = (isObject(x) ? Object.assign({}, x) : {});
        } else {
            throw 'invalid path';
        }
        x[first] = change(rest, x[first]);
        return x;
    })(flatten(path), x);
});

/**
 * Replace value referenced with path with another value
 * (curried function)
 *
 * @function
 * @sig Path -> (a -> b) -> c -> c
 * @param {Path} path
 * @param {*} val
 * @param {*} x
 * @return {*}
 */
const set = curry((path, val, x) => change(path, _ => val, x));

/**
 * Omitting value referenced by path
 * (curried function)
 *
 * @function
 * @sig Path -> a -> a
 * @param {Path} path
 * @param {*} x
 * @return {*}
 */
const omit = curry((path, x) => {
    function _omit(path, x) {
        if (isInteger(path[0])) {
            x = (isArray(x) ? Array.from(x) : []);
        } else if (isString(path[0])) {
            x = (isObject(x) ? Object.assign({}, x) : {});
        } else {
            throw 'invalid path';
        }
        if (path.length > 1) {
            x[path[0]] = _omit(path.slice(1), x[path[0]]);
        } else if (isInteger(path[0])) {
            x.splice(path[0], 1);
        } else {
            delete x[path[0]];
        }
        return x;
    }
    path = flatten(path);
    if (path.length < 1)
        return undefined;
    return _omit(path, x);
});

/**
 * Change by moving value from source path to destination path
 * (curried function)
 *
 * @function
 * @sig Path -> Path -> a -> a
 * @param {Path} srcPath
 * @param {Path} dstPath
 * @param {*} x
 * @return {*}
 */
const move = curry((srcPath, dstPath, x) => pipe(
    set(dstPath, get(srcPath, x)),
    omit(srcPath)
)(x));

/**
 * Sort array
 * (curried function)
 *
 * Comparison function receives two arguments representing array elements and
 * should return:
 *   - negative number in case first argument is more significant then second
 *   - zero in case first argument is equaly significant as second
 *   - positive number in case first argument is less significant then second
 *
 * @function
 * @sig ((a, a) -> Number) -> [a] -> [a]
 * @param {Function} fn
 * @param {Array} arr
 * @return {Array}
 */
const sort = curry((fn, arr) => Array.from(arr).sort(fn));

/**
 * Sort array based on results of appling function to it's elements
 * (curried function)
 *
 * Resulting order is determined by comparring function application results
 * with greater then and lesser then operators.
 *
 * @function
 * @sig (a -> b) -> [a] -> [a]
 * @param {Function} fn
 * @param {Array} arr
 * @return {Array}
 */
const sortBy = curry((fn, arr) => sort((x, y) => {
    const xVal = fn(x);
    const yVal = fn(y);
    if (xVal < yVal)
        return -1;
    if (xVal > yVal)
        return 1;
    return 0;
}, arr));

/**
 * Create object containing only subset of selected properties
 * (curried function)
 *
 * @function
 * @sig [String] -> a -> a
 * @param {Array} arr
 * @param {Object} obj
 * @return {Object}
 */
const pick = curry((arr, obj) => {
    const ret = {};
    for (let i of arr)
        if (i in obj)
            ret[i] = obj[i];
    return ret;
});

/**
 * Change array or object by appling function to it's elements
 * (curried function)
 *
 * For each element, provided function is called with element value,
 * index/key and original container.
 *
 * @function
 * @sig ((a, Number, [a]) -> b) -> [a] -> [b]
 * @sig ((a, String, {String: a}) -> b) -> {String: a} -> {String: b}
 * @param {Function} fn
 * @param {Array|Object} x
 * @return {Array|Object}
 */
const map = curry((fn, x) => {
    if (isArray(x))
        return x.map(fn);
    const res = {};
    for (let k in x)
        res[k] = fn(x[k], k, x);
    return res;
});

/**
 * Change array to contain only elements for which function returns `true`
 * (curried function)
 *
 * @function
 * @sig (a -> Boolean) -> [a] -> [a]
 * @param {Function} fn
 * @param {Array} arr
 * @return {Array}
 */
const filter = curry((fn, arr) => arr.filter(fn));

/**
 * Append value to end of array
 * (curried function)
 *
 * @function
 * @sig a -> [a] -> [a]
 * @param {*} val
 * @param {Array} arr
 * @return {Array}
 */
const append = curry((val, arr) => arr.concat([val]));

/**
 * Reduce array or object by appling function
 * (curried function)
 *
 * For each element, provided function is called with accumulator,
 * elements value, element index/key and original container.
 *
 * @function
 * @sig ((b, a, Number, [a]) -> b) -> b -> [a] -> b
 * @sig ((b, a, String, {String: a}) -> b) -> b -> {String: a} -> b
 * @param {Function} fn
 * @param {*} val initial accumulator value
 * @param {Array|Object} x
 * @return {*} reduced value
 */
const reduce = curry((fn, val, x) => {
    if (isArray(x))
        return x.reduce(fn, val);
    let acc = val;
    for (let k in x)
        acc = fn(acc, x[k], k, x);
    return acc;
});

/**
 * Merge two objects
 * (curried function)
 *
 * If same property exist in both arguments, second argument's value is used
 * as resulting value
 *
 * @function
 * @sig a -> a -> a
 * @param {Object} x
 * @param {Object} y
 * @return {Object}
 */
const merge = curry((x, y) => Object.assign({}, x, y));

/**
 * Merge multiple objects
 * (curried function)
 *
 * If same property exist in multiple arguments, value from the last argument
 * containing that property is used
 *
 * @function
 * @sig [a] -> a
 * @param {Object[]}
 * @return {Object}
 */
const mergeAll = reduce(merge, {});

/**
 * Find element in array or object for which provided function returns `true`
 * (curried function)
 *
 * Until element is found, provided function is called for each element with
 * arguments: current element, current index/key and initial container.
 *
 * If searched element is not found, `undefined` is returned.
 *
 * @function
 * @sig ((a, Number, [a]) -> Boolean) -> [a] -> a
 * @sig ((a, String, {String: a}) -> Boolean) -> {String: a} -> a
 * @param {Function} fn
 * @param {Array|Object} x
 * @return {*}
 */
const find = curry((fn, x) => {
    if (isArray(x))
        return x.find(fn);
    for (let k in x)
        if (fn(x[k], k, x))
            return x[k];
});

/**
 * Find element's index/key in array or object for which provided function
 * returns `true`
 * (curried function)
 *
 * Until element is found, provided function is called for each element with
 * arguments: current element, current index/key and initial container.
 *
 * If searched element is not found, `undefined` is returned.
 *
 * @function
 * @sig ((a, Number, [a]) -> Boolean) -> [a] -> a
 * @sig ((a, String, {String: a}) -> Boolean) -> {String: a} -> a
 * @param {Function} fn
 * @param {Array|Object} x
 * @return {*}
 */
const findIndex = curry((fn, x) => {
    if (isArray(x))
        return x.findIndex(fn);
    for (let k in x)
        if (fn(x[k], k, x))
            return k;
});

/**
 * Concatenate two arrays
 * (curried function)
 *
 * @function
 * @sig [a] -> [a] -> [a]
 * @param {Array} x
 * @param {Array} y
 * @return {Array}
 */
const concat = curry((x, y) => x.concat(y));

/**
 * Create union of two arrays using `equals` to check equality
 * (curried function)
 *
 * @function
 * @sig [a] -> [a] -> [a]
 * @param {Array} x
 * @param {Array} y
 * @return {Array}
 */
const union = curry((x, y) => {
    return reduce((acc, val) => {
        if (!find(equals(val), x))
            acc = append(val, acc);
        return acc;
    }, x, y);
});

/**
 * Check if array contains value
 * (curried function)
 *
 * TODO: add support for objects (should we check for keys or values?)
 *
 * @function
 * @sig a -> [a] -> Boolean
 * @param {*} val
 * @param {Array|Object} x
 * @return {Boolean}
 */
const contains = curry((val, arr) => arr.includes(val));

/**
 * Insert value into array on specified index
 * (curried function)
 *
 * @function
 * @sig Number -> a -> [a] -> [a]
 * @param {Number} idx
 * @param {*} val
 * @param {Array} arr
 * @return {Array}
 */
const insert = curry((idx, val, arr) =>
    arr.slice(0, idx).concat([val], arr.slice(idx)));

/**
 * Get array slice
 * (curried function)
 *
 * @function
 * @sig Number -> Number -> [a] -> [a]
 * @param {Number} begin
 * @param {Number} end
 * @param {Array} arr
 * @return {Array}
 */
const slice = curry((begin, end, arr) => arr.slice(begin, end));

/**
 * Reverse array
 *
 * @function
 * @sig [a] -> [a]
 * @param  {Array} arr
 * @return {Array}
 */
function reverse(arr) {
    return Array.from(arr).reverse();
}

/**
 * Array length
 *
 * @function
 * @sig [a] -> Number
 * @param  {Array} arr
 * @return {Number}
 */
function length(arr) {
    return arr.length;
}

/**
 * Increment value
 * @param  {Number} val
 * @return {Number}
 */
function inc(val) {
    return val + 1;
}

/**
 * Decrement value
 * @param  {Number} val
 * @return {Number}
 */
function dec(val) {
    return val - 1;
}

/**
 * Logical not
 * @param  {Any} val
 * @return {Boolean}
 */
function not(val) {
    return !val;
}

/**
 * Create promise that resolves in `t` milliseconds
 *
 * TODO: move to other module
 *
 * @function
 * @sig Number -> Promise
 * @param {Number} t
 * @return {Promise}
 */
function sleep(t) {
    return new Promise(resolve => {
        setTimeout(() => { resolve(); }, t);
    });
}

/**
 * Delay function call `fn(...args)` for `t` milliseconds
 *
 * TODO: move to other module
 *
 * @function
 * @sig (((a1, a2, ..., an) -> _), Number, a1, a2, ..., an) -> Promise
 * @param {Function} fn
 * @param {Number} [t=0]
 * @param {*} args
 * @return {Promise}
 */
function delay(fn, t, ...args) {
    return new Promise(resolve => {
        setTimeout(() => { resolve(fn(...args)); }, t || 0);
    });
}


/***/ }),
/* 12 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "state": () => (/* binding */ state),
/* harmony export */   "init": () => (/* binding */ init),
/* harmony export */   "timestampToString": () => (/* binding */ timestampToString)
/* harmony export */ });
/* harmony import */ var _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1);



const localTimezoneOffset = (new Date()).getTimezoneOffset() * 60;


const state = {
    entries: []
};


function init() {
    fetch('/entries').then(response =>
        response.json()
    ).then(data =>
        _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__.default.set('entries', data['entries'])
    );
}


function timestampToString(timestamp) {
    const date = new Date((timestamp - localTimezoneOffset) * 1000);
    return date.toISOString().replace('T', ' ').replace('Z', '');
}


/***/ }),
/* 13 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "main": () => (/* binding */ main)
/* harmony export */ });
/* harmony import */ var _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1);
/* harmony import */ var _hat_core_util__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(11);
/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(12);






function main() {
    const entries = _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__.default.get('entries');

    return ['div.main',
        ['table',
            ['thead',
                ['tr',
                    ['th.col-id', 'ID'],
                    ['th.col-time', 'Time'],
                    ['th.col-address', 'Address'],
                    ['th.col-source', 'Source'],
                    ['th.col-type', 'Type'],
                    ['th.col-data', 'Data']
                ]
            ],
            ['tbody', entries.map(entry =>
                ['tr',
                    ['td.col-id', String(entry.entry_id)],
                    ['td.col-time', _common__WEBPACK_IMPORTED_MODULE_2__.timestampToString(entry.timestamp)],
                    ['td.col-address', String(entry.address)],
                    ['td.col-source', String(entry.source)],
                    ['td.col-type', String(entry.type)],
                    ['td.col-data', data(entry.type, entry.data)]
                ]
            )]
        ]
    ];
}


function data(type, data) {
    if (type == 'builtin.status.linux')
        return builtinStatusLinux(data);

    return JSON.stringify(data);
}


function builtinStatusLinux(data) {
    const timestamp = _hat_core_util__WEBPACK_IMPORTED_MODULE_1__.get('timestamp', data);
    const uptime = _hat_core_util__WEBPACK_IMPORTED_MODULE_1__.get('uptime', data);
    const thermal = _hat_core_util__WEBPACK_IMPORTED_MODULE_1__.get('thermal', data) || [];
    const disks = _hat_core_util__WEBPACK_IMPORTED_MODULE_1__.get('disks', data) || [];

    return ['div.data',
        ['label', 'Time:'],
        ['span', _common__WEBPACK_IMPORTED_MODULE_2__.timestampToString(timestamp)],
        ['label', 'Uptime:'],
        ['span', `${uptime}s`],
        thermal.map(i => [
            ['label', `Temp - ${i.type}:`],
            ['span', `${i.temp}°C`]
        ]),
        disks.map(i => [
            ['label', `Disk - ${i.name}:`],
            ['span', `${i.percent} (${i.used}/${i.size})`]
        ]),
    ];
}


/***/ }),
/* 14 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(15);
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_node_modules_resolve_url_loader_index_js_node_modules_sass_loader_dist_cjs_js_ruleSet_1_rules_0_use_3_main_scss__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(16);

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_node_modules_resolve_url_loader_index_js_node_modules_sass_loader_dist_cjs_js_ruleSet_1_rules_0_use_3_main_scss__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_node_modules_resolve_url_loader_index_js_node_modules_sass_loader_dist_cjs_js_ruleSet_1_rules_0_use_3_main_scss__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ }),
/* 15 */
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),
/* 16 */
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(17);
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(18);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "html, body {\n  font-family: sans-serif;\n  font-size: 12pt;\n  margin: 0;\n  height: 100%;\n}\n\nbody > .main > table {\n  width: 100%;\n  border-spacing: 0;\n  table-layout: fixed;\n  position: relative;\n}\nbody > .main > table th {\n  padding: 0.4rem;\n  background: #616161;\n  color: whitesmoke;\n  position: sticky;\n  top: 0;\n}\nbody > .main > table tr:nth-child(even) {\n  background-color: #e0e0e0;\n}\nbody > .main > table tr:nth-child(odd) {\n  background-color: whitesmoke;\n}\nbody > .main > table td {\n  padding: 0.2rem;\n  vertical-align: top;\n}\nbody > .main > table .col-id {\n  width: 5rem;\n}\nbody > .main > table .col-time {\n  width: 12rem;\n}\nbody > .main > table .col-address {\n  width: 10rem;\n}\nbody > .main > table .col-source {\n  width: 10rem;\n}\nbody > .main > table .col-type {\n  width: 10rem;\n}\nbody > .main > table td.col-id {\n  text-align: center;\n}\nbody > .main > table td.col-data > .data {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, 15rem 15rem);\n  grid-gap: 0.3rem;\n  align-items: center;\n}\nbody > .main > table td.col-data > .data > label {\n  justify-self: end;\n}", "",{"version":3,"sources":["webpack://./main.scss"],"names":[],"mappings":"AAaA;EACI,uBAAA;EACA,eAAA;EACA,SAAA;EACA,YAAA;AAZJ;;AAgBI;EACI,WAAA;EACA,iBAAA;EACA,mBAAA;EACA,kBAAA;AAbR;AAeQ;EACI,eAAA;EACA,mBArBK;EAsBL,iBA5BK;EA6BL,gBAAA;EACA,MAAA;AAbZ;AAiBY;EACI,yBAjCC;AAkBjB;AAkBY;EACI,4BAvCC;AAuBjB;AAoBQ;EACI,eAAA;EACA,mBAAA;AAlBZ;AAqBQ;EAAU,WAAA;AAlBlB;AAmBQ;EAAY,YAAA;AAhBpB;AAiBQ;EAAe,YAAA;AAdvB;AAeQ;EAAc,YAAA;AAZtB;AAaQ;EAAY,YAAA;AAVpB;AAYQ;EACI,kBAAA;AAVZ;AAcY;EACI,aAAA;EACA,oDAAA;EACA,gBAAA;EACA,mBAAA;AAZhB;AAcgB;EACI,iBAAA;AAZpB","sourcesContent":["\n$color-grey-50: rgb(250, 250, 250);\n$color-grey-100: rgb(245, 245, 245);\n$color-grey-200: rgb(238, 238, 238);\n$color-grey-300: rgb(224, 224, 224);\n$color-grey-400: rgb(189, 189, 189);\n$color-grey-500: rgb(158, 158, 158);\n$color-grey-600: rgb(117, 117, 117);\n$color-grey-700: rgb(97, 97, 97);\n$color-grey-800: rgb(66, 66, 66);\n$color-grey-900: rgb(33, 33, 33);\n\n\nhtml, body {\n    font-family: sans-serif;\n    font-size: 12pt;\n    margin: 0;\n    height: 100%;\n}\n\nbody > .main {\n    & > table {\n        width: 100%;\n        border-spacing: 0;\n        table-layout: fixed;\n        position: relative;\n\n        th {\n            padding: 0.4rem;\n            background: $color-grey-700;\n            color: $color-grey-100;\n            position: sticky;\n            top: 0;\n        }\n\n        tr {\n            &:nth-child(even) {\n                background-color: $color-grey-300;\n            }\n\n            &:nth-child(odd) {\n                background-color: $color-grey-100;\n            }\n        }\n\n        td {\n            padding: 0.2rem;\n            vertical-align: top;\n        }\n\n        .col-id { width: 5rem; }\n        .col-time { width: 12rem; }\n        .col-address { width: 10rem; }\n        .col-source { width: 10rem; }\n        .col-type { width: 10rem; }\n\n        td.col-id {\n            text-align: center;\n        }\n\n        td.col-data {\n            & > .data {\n                display: grid;\n                grid-template-columns: repeat(auto-fit, 15rem 15rem);\n                grid-gap: 0.3rem;\n                align-items: center;\n\n                & > label {\n                    justify-self: end;\n                }\n            }\n        }\n    }\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),
/* 17 */
/***/ ((module) => {



function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

module.exports = function cssWithMappingToString(item) {
  var _item = _slicedToArray(item, 4),
      content = _item[1],
      cssMapping = _item[3];

  if (typeof btoa === "function") {
    // eslint-disable-next-line no-undef
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || "").concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join("\n");
  }

  return [content].join("\n");
};

/***/ }),
/* 18 */
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (cssWithMappingToString) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join("");
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === "string") {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, ""]];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

/***/ })
/******/ 	]);
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		if(__webpack_module_cache__[moduleId]) {
/******/ 			return __webpack_module_cache__[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1);
/* harmony import */ var _hat_core_util__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(11);
/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(12);
/* harmony import */ var _vt__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(13);
/* harmony import */ var main_scss__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(14);









function main() {
    const root = document.body.appendChild(document.createElement('div'));
    _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__.default.init(root, _common__WEBPACK_IMPORTED_MODULE_2__.state, _vt__WEBPACK_IMPORTED_MODULE_3__.main);
    _common__WEBPACK_IMPORTED_MODULE_2__.init();
}


window.addEventListener('load', main);
window.r = _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__.default;
window.u = _hat_core_util__WEBPACK_IMPORTED_MODULE_1__;

})();

/******/ })()
;
//# sourceMappingURL=index.js.map