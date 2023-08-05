"use strict";
(self["webpackChunkjupyterlab_autoscrollcelloutput"] = self["webpackChunkjupyterlab_autoscrollcelloutput"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ButtonAutoScrollCellOutput": () => (/* binding */ ButtonAutoScrollCellOutput),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);


function JupyterLabAutoScroll() {
    let divs = document.querySelectorAll('.lm-Widget.p-Widget.jp-OutputArea.jp-Cell-outputArea');
    for (let i = 0; i < divs.length; i++) {
        let div = divs[i];
        if (div.scrollHeight > 0 &&
            div.scrollTop != div.scrollHeight &&
            div.parentElement != null &&
            div.parentElement.parentElement != null &&
            div.parentElement.parentElement.childNodes[1].childNodes[1].childNodes[0].childNodes[0].textContent == "[*]:") {
            if (div.childNodes.length == 1) {
                div.scrollTop = div.scrollHeight;
            }
        }
    }
}
/**
 * Initialization data for the jupyterlab_autoscrollcelloutput extension.
 */
const plugin = {
    id: 'jupyterlab_autoscrollcelloutput:plugin',
    autoStart: true,
    activate: (app) => {
        console.log('JupyterLab extension jupyterlab_autoscrollcelloutput is activated!');
        app.docRegistry.addWidgetExtension('Notebook', new ButtonAutoScrollCellOutput());
    }
};
class ButtonAutoScrollCellOutput {
    createNew(panel, context) {
        const triggerAutoScrollCellOutput = () => {
            if (SET) {
                SET = false;
                if (button.hasClass('selected'))
                    button.removeClass('selected');
                clearInterval(t);
            }
            else {
                SET = true;
                button.addClass('selected');
                t = setInterval(JupyterLabAutoScroll, 10);
            }
        };
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            className: 'buttonAutoScrollCellOuput',
            iconClass: 'wll-ScrollIcon',
            label: 'scroll',
            onClick: triggerAutoScrollCellOutput,
            tooltip: 'Auto Scroll Cell Ouput'
        });
        panel.toolbar.insertItem(10, 'AutoScrollCellOutput', button);
        var SET = true;
        var t = setInterval(JupyterLabAutoScroll, 10);
        button.addClass('selected');
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__.DisposableDelegate(() => { button.dispose(); });
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.b14d597ae4cb174b94ed.js.map