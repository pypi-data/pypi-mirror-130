"use strict";
(self["webpackChunkpi_lab_jupyter_extension"] = self["webpackChunkpi_lab_jupyter_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _plugin_cell_tool_bar__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./plugin_cell_tool_bar */ "./lib/plugin_cell_tool_bar.js");
/* harmony import */ var _plugin_ppt_view__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./plugin_ppt_view */ "./lib/plugin_ppt_view.js");
/* harmony import */ var _plugin_pi_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./plugin_pi_notebook */ "./lib/plugin_pi_notebook.js");



const plugins = [
    _plugin_cell_tool_bar__WEBPACK_IMPORTED_MODULE_0__.cellToolBarPlugin,
    _plugin_ppt_view__WEBPACK_IMPORTED_MODULE_1__.pptViewPlugin,
    _plugin_pi_notebook__WEBPACK_IMPORTED_MODULE_2__.piNotebookPlugin,
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/plugin_cell_tool_bar.js":
/*!*************************************!*\
  !*** ./lib/plugin_cell_tool_bar.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "cellToolBarPlugin": () => (/* binding */ cellToolBarPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _style_cell_tool_bar_run_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/cell_tool_bar/run.svg */ "./style/cell_tool_bar/run.svg");
/* harmony import */ var _style_cell_tool_bar_code_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/cell_tool_bar/code.svg */ "./style/cell_tool_bar/code.svg");
/* harmony import */ var _style_cell_tool_bar_delete_svg__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/cell_tool_bar/delete.svg */ "./style/cell_tool_bar/delete.svg");
/* harmony import */ var _style_cell_tool_bar_format_svg__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/cell_tool_bar/format.svg */ "./style/cell_tool_bar/format.svg");
// import React from 'react';








const EXTENSION_ID = 'pi_lab_jupyter_extension:cell_tool_bar_plugin';
const CELL_BAR_CLASS = 'jp-pilab-cell-toobar-pulgin-tool-bar';
const runIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
    name: `${EXTENSION_ID}:run`,
    svgstr: _style_cell_tool_bar_run_svg__WEBPACK_IMPORTED_MODULE_4__["default"]
});
const codeIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
    name: `${EXTENSION_ID}:code`,
    svgstr: _style_cell_tool_bar_code_svg__WEBPACK_IMPORTED_MODULE_5__["default"]
});
const deleteIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
    name: `${EXTENSION_ID}:delete`,
    svgstr: _style_cell_tool_bar_delete_svg__WEBPACK_IMPORTED_MODULE_6__["default"]
});
const formatIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
    name: `${EXTENSION_ID}:format`,
    svgstr: _style_cell_tool_bar_format_svg__WEBPACK_IMPORTED_MODULE_7__["default"]
});
// function getCSSVar(name: string): string {
//   return getComputedStyle(document.documentElement)
//     .getPropertyValue(name)
//     .trim();
// }
const DEFAULT_LEFT_MENU = [
    // Originate from @jupyterlab/notebook-extension
    {
        command: 'notebook:run-cell-and-select-next',
        icon: runIcon
    },
    {
        command: 'notebook:move-cell-up',
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.caretUpEmptyThinIcon
    },
    {
        command: 'notebook:move-cell-down',
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.caretDownEmptyThinIcon
    },
    {
        command: 'notebook:insert-cell-below',
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.addIcon
    },
    {
        cellType: 'markdown',
        command: 'notebook:change-cell-to-code',
        icon: codeIcon
    },
    {
        cellType: 'code',
        command: 'notebook:change-cell-to-markdown',
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.markdownIcon
    },
    // Originate from @ryantam626/jupyterlab_code_formatter  必须安装jupyterlab_code_formatter 插件才可用
    {
        cellType: 'code',
        command: 'jupyterlab_code_formatter:format',
        icon: formatIcon,
        tooltip: '格式化代码'
    },
];
const DEFAULT_RIGHT_MENU = [
    // Originate from @jupyterlab/notebook-extension
    {
        command: 'notebook:delete-cell',
        icon: deleteIcon
    }
];
/**
 * Toolbar icon menu container
 */
class CellMenu extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor(commands, items) {
        super();
        this._commands = commands;
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.PanelLayout();
        this.addClass('jp-pilab-cell-toobar-pulgin-menu');
        this._addButtons(items);
    }
    handleEvent(event) {
        switch (event.type) {
            case 'mousedown':
            case 'click':
                // Ensure the mouse event is not propagated on the cell.
                // As buttons are hidden except on the selected cell, this is fine.
                event.stopPropagation();
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach() {
        this.node.addEventListener('mousedown', this);
        this.node.addEventListener('click', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach() {
        this.node.removeEventListener('mousedown', this);
        this.node.removeEventListener('click', this);
    }
    _addButtons(items) {
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.each)(this.children(), widget => {
            widget.dispose();
        });
        const layout = this.layout;
        items.forEach(entry => {
            var _a, _b;
            if (this._commands.hasCommand(entry.command)) {
                layout.addWidget(new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
                    icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon.resolve({ icon: entry.icon }),
                    className: `jp-pilab-cell-toobar-pulgin-${(_a = entry.cellType) !== null && _a !== void 0 ? _a : 'all'}`,
                    onClick: () => {
                        this._commands.execute(entry.command);
                    },
                    tooltip: (_b = entry.tooltip) !== null && _b !== void 0 ? _b : this._commands.label(entry.command)
                }));
            }
        });
    }
}
/**
 * Cell 上方工具栏(ToolBar) Widget
 */
class CellToolbarWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor(commands, leftMenuItems, rightMenuItems) {
        super();
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.PanelLayout();
        this.addClass('jp-pilab-cell-toobar-pulgin-toolbar');
        this.layout.addWidget(new CellMenu(commands, leftMenuItems));
        // 顶部固定布局
        // const leftSpace = 0;
        // this.node.style.position = 'absolute';
        // this.node.style.left = `${leftSpace}px`;
        // this.node.style.top = '0px';
        // this.node.style.width = `calc( 100% - ${leftSpace}px - ${getCSSVar(
        //   '--jp-cell-collapser-width'
        // )} - ${getCSSVar('--jp-cell-prompt-width')} - ${getCSSVar(
        //   '--jp-cell-padding'
        // )} )`;
        // 右侧浮动布局
        const right = 30;
        const top = 24;
        this.node.style.position = 'absolute';
        this.node.style.right = `${right}px`;
        this.node.style.top = `${top}px`;
        this.node.style.justifyContent = 'flex-end';
        this.node.style.width = 'max-content';
        this.addClass('jp-overlap');
        this.layout.addWidget(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar.createSpacerItem());
        this.layout.addWidget(new CellMenu(commands, rightMenuItems));
    }
}
/**
 * CellToolbarTracker
 */
class CellToolbarTracker {
    constructor(panel, commands) {
        this._isDisposed = false;
        this._commands = commands;
        this._panel = panel;
        // find(panel.toolbar.children(), (tbb, index) => {
        //   return tbb.hasClass('jp-Notebook-toolbarCellType');
        // });
        const cells = this._panel.context.model.cells;
        cells.changed.connect(this.updateConnectedCells, this);
        panel.context.fileChanged.connect(this._onFileChanged, this);
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        var _a, _b;
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        const cells = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.context.model.cells;
        if (cells) {
            cells.changed.disconnect(this.updateConnectedCells, this);
            (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.each)(cells.iter(), model => this._removeToolbar(model));
        }
        (_b = this._panel) === null || _b === void 0 ? void 0 : _b.context.fileChanged.disconnect(this._onFileChanged);
        this._panel = null;
    }
    updateConnectedCells(cells, changed) {
        changed.oldValues.forEach(model => this._removeToolbar(model));
        changed.newValues.forEach(model => this._addToolbar(model));
    }
    _addToolbar(model) {
        const cell = this._getCell(model);
        if (cell) {
            const leftMenu = DEFAULT_LEFT_MENU;
            const rightMenu = DEFAULT_RIGHT_MENU;
            const toolbar = new CellToolbarWidget(this._commands, leftMenu, rightMenu);
            toolbar.addClass(CELL_BAR_CLASS);
            cell.layout.insertWidget(0, toolbar);
        }
    }
    _getCell(model) {
        var _a;
        return (_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.widgets.find(widget => widget.model === model);
    }
    _findToolbarWidgets(cell) {
        const widgets = cell.layout.widgets;
        // Search for header using the CSS class or use the first one if not found.
        return widgets.filter(widget => widget.hasClass(CELL_BAR_CLASS)) || [];
    }
    _removeToolbar(model) {
        const cell = this._getCell(model);
        if (cell) {
            this._findToolbarWidgets(cell).forEach(widget => widget.dispose());
        }
    }
    _onFileChanged() {
    }
}
/**
 * CellBarExtension
 */
class CellBarExtension {
    constructor(commands) {
        this._commands = commands;
    }
    createNew(panel) {
        // 每当创建一个 Cell 时, 为其添加一个 CellToolbarTracker
        return new CellToolbarTracker(panel, this._commands);
    }
}
/**
 * Plugin
 */
const cellToolBarPlugin = {
    id: EXTENSION_ID,
    autoStart: true,
    activate: async (app) => {
        console.log(`插件 ${EXTENSION_ID} 已激活.`);
        // 每当打开一个 notebook 时, 创建一个 CellBarExtension
        app.docRegistry.addWidgetExtension('Notebook', new CellBarExtension(app.commands));
    },
};


/***/ }),

/***/ "./lib/plugin_pi_notebook.js":
/*!***********************************!*\
  !*** ./lib/plugin_pi_notebook.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "piNotebookPlugin": () => (/* binding */ piNotebookPlugin)
/* harmony export */ });
/**
 * PiNotebookTracker
 */
class PiNotebookTracker {
    constructor(panel) {
        this._isDisposed = false;
        this._panel = panel;
        const cells = this._panel.context.model.cells;
        cells.changed.connect(this.updateConnectedCells, this);
        panel.context.fileChanged.connect(this._onFileChanged, this);
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        var _a, _b;
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        const cells = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.context.model.cells;
        if (cells) {
            cells.changed.disconnect(this.updateConnectedCells, this);
        }
        (_b = this._panel) === null || _b === void 0 ? void 0 : _b.context.fileChanged.disconnect(this._onFileChanged);
        this._panel = null;
    }
    updateConnectedCells(cells, changed) {
        // changed.oldValues.forEach(model => this._removeToolbar(model));
        // changed.newValues.forEach(model => this._addToolbar(model));
    }
    _onFileChanged() {
        console.log('文件变更.');
    }
}
/**
 * PiNotebookExtension
 */
class PiNotebookExtension {
    createNew(panel) {
        // 每当创建一个 Cell 时, 为其添加一个 PiNotebookTracker
        return new PiNotebookTracker(panel);
    }
}
/**
 * Pi Notebook Plugin
 */
const piNotebookPlugin = {
    id: 'pi_lab_jupyter_extension:pi_notebook_plugin',
    autoStart: true,
    activate: (app) => {
        console.log('插件 pi_lab_jupyter_extension:pi_notebook_plugin 已激活.');
        // 每当打开一个 notebook 时, 创建一个 PiNotebookExtension
        app.docRegistry.addWidgetExtension('Notebook', new PiNotebookExtension());
    }
};


/***/ }),

/***/ "./lib/plugin_ppt_view.js":
/*!********************************!*\
  !*** ./lib/plugin_ppt_view.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "pptViewPlugin": () => (/* binding */ pptViewPlugin)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _style_ppt_view_loading_gif__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/ppt_view/loading.gif */ "./style/ppt_view/loading.gif");
/* harmony import */ var _style_ppt_view_ppt_view_svg__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../style/ppt_view/ppt-view.svg */ "./style/ppt_view/ppt-view.svg");









const subWindowRef = react__WEBPACK_IMPORTED_MODULE_0___default().createRef();
let observer;
/**
 * PPTComponent
 * @param props
 * @returns
 */
const PPTComponent = (props) => {
    const [showLoading, setShowLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
    let needDisplay;
    let canBeDistroy;
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        console.log(`path: ${props.path}`);
        console.log('create PPTComponent...');
        needDisplay = true;
        canBeDistroy = false;
        return function cleanup() {
            console.log('destroy PPTComponent...');
        };
    });
    const startRise = () => {
        const subDocument = window.notebook.document;
        const config = { attributes: false, childList: true, subtree: true };
        const callback = (mutationRecords, observer) => {
            for (let mutationRecord of mutationRecords) {
                if (mutationRecord.type === 'childList') {
                    // const node: Node = mutationRecord.target;
                    if (needDisplay) {
                        const riseBtn = window.notebook.document.getElementById('RISE');
                        if (riseBtn) {
                            console.log('start RISE...');
                            setShowLoading(false);
                            riseBtn.click();
                            subWindowRef.current.style.width = '100%';
                            subWindowRef.current.style.height = '100%';
                            needDisplay = false;
                            canBeDistroy = true;
                            break;
                        }
                    }
                    else if (canBeDistroy) {
                        const exitBtn = window.notebook.document.getElementById('exit_b');
                        if (!exitBtn) {
                            console.log('exit RISE...');
                            observer.disconnect();
                            canBeDistroy = false;
                            subWindowRef.current.style.width = '0';
                            subWindowRef.current.style.height = '0';
                            props.close();
                        }
                    }
                }
            }
        };
        observer = new MutationObserver(callback);
        observer.observe(subDocument.body, config);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { "height": "100vh", "width": "100vw", "background": "rgba(0,0,0,0.45)" } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { ref: subWindowRef, style: { "height": "0", "width": "0" } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("iframe", { name: "notebook", src: props.path, 
                // src="http://simeondemacbook-pro.local:8888/notebooks/files/matplotlib.tmp-ipynb.ipynb"
                height: "100%", width: "100%", scrolling: "auto", frameBorder: "0", onLoad: () => startRise() })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("img", { src: _style_ppt_view_loading_gif__WEBPACK_IMPORTED_MODULE_7__["default"], style: {
                display: showLoading ? "block" : "none",
                "height": "80px", "width": "80px", "position": "fixed", "top": "48%", "left": "48%"
            } })));
};
/**
 * PPTTabWidget
 */
class PPTTabWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    constructor(context) {
        super();
        this.addClass('ppt-widgets-view');
        this.id = 'ppt-widget';
        this.context = context;
    }
    gen_notebook_url() {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_6__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.URLExt.join(settings.baseUrl, 'notebooks', this.context.path);
        return url;
    }
    close() {
        console.log('revert');
        this.context.revert();
        super.close();
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(PPTComponent, { path: this.gen_notebook_url(), close: () => this.close() }));
    }
}
/**
 * PPT view button
 */
class PPTViewButton {
    createNew(panel, context) {
        const icon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon({
            name: 'launcher:ppt-view-icon',
            svgstr: _style_ppt_view_ppt_view_svg__WEBPACK_IMPORTED_MODULE_8__["default"],
        });
        const openPPTView = () => {
            const pptWidget = new PPTTabWidget(context);
            _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget.attach(pptWidget, document.body);
        };
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            className: 'ppt-view-button',
            icon: icon,
            tooltip: 'PPT',
            onClick: openPPTView,
        });
        panel.toolbar.insertItem(10, 'openPPTViews', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
/**
 * Initialization data for the @pi-lab-extension/ppt-view extension.
 */
const pptViewPlugin = {
    id: 'pi_lab_jupyter_extension:ppt_view_plugin',
    autoStart: true,
    activate: (app) => {
        console.log('插件 pi_lab_jupyter_extension:ppt_view_plugin 已激活.');
        app.docRegistry.addWidgetExtension('Notebook', new PPTViewButton());
    }
};


/***/ }),

/***/ "./style/ppt_view/loading.gif":
/*!************************************!*\
  !*** ./style/ppt_view/loading.gif ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (__webpack_require__.p + "a5dd3bc133cc9f5d9a9170539c2f7dfec933b9ab7c02eeb7a761bbd97d22d3ff.gif");

/***/ }),

/***/ "./style/cell_tool_bar/code.svg":
/*!**************************************!*\
  !*** ./style/cell_tool_bar/code.svg ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"16px\" height=\"16px\">\n    <path d=\"M0 0h24v24H0V0z\" fill=\"none\" />\n    <path class=\"jp-icon3\" fill=\"#626262\" d=\"M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z\" />\n</svg>");

/***/ }),

/***/ "./style/cell_tool_bar/delete.svg":
/*!****************************************!*\
  !*** ./style/cell_tool_bar/delete.svg ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"16px\" height=\"16px\">\n    <path d=\"M0 0h24v24H0z\" fill=\"none\" />\n    <path class=\"jp-icon3\" fill=\"#626262\" d=\"M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z\" />\n</svg>");

/***/ }),

/***/ "./style/cell_tool_bar/format.svg":
/*!****************************************!*\
  !*** ./style/cell_tool_bar/format.svg ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" focusable=\"false\" width=\"16px\"\n    height=\"16px\" style=\"-ms-transform: rotate(360deg); -webkit-transform: rotate(360deg); transform: rotate(360deg);\"\n    preserveAspectRatio=\"xMidYMid meet\" viewBox=\"0 0 1792 1792\">\n    <path class=\"jp-icon3\"\n        d=\"M1473 929q7-118-33-226.5t-113-189t-177-131T929 325q-116-7-225.5 32t-192 110.5t-135 175T317 863q-7 118 33 226.5t113 189t177.5 131T862 1467q155 9 293-59t224-195.5t94-283.5zM1792 0l-349 348q120 117 180.5 272t50.5 321q-11 183-102 339t-241 255.5T999 1660L0 1792l347-347q-120-116-180.5-271.5T116 852q11-184 102-340t241.5-255.5T792 132q167-22 500-66t500-66z\"\n        fill=\"#626262\" />\n</svg>");

/***/ }),

/***/ "./style/cell_tool_bar/run.svg":
/*!*************************************!*\
  !*** ./style/cell_tool_bar/run.svg ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg t=\"1638817238880\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" p-id=\"2485\"\n    width=\"200\" height=\"200\">\n    <path\n        d=\"M512 0a512 512 0 1 0 512 512 512.585143 512.585143 0 0 0-512-512z m0 945.225143A433.225143 433.225143 0 1 1 945.225143 512 433.737143 433.737143 0 0 1 512 945.225143z\"\n        p-id=\"2486\"></path>\n    <path\n        d=\"M445.147429 263.899429a42.203429 42.203429 0 0 0-66.998858 34.157714v448.073143a42.203429 42.203429 0 0 0 66.998858 34.084571l308.077714-224.036571a42.203429 42.203429 0 0 0 0-68.242286L445.147429 263.972571z\"\n        p-id=\"2487\"></path>\n</svg>\n");

/***/ }),

/***/ "./style/ppt_view/ppt-view.svg":
/*!*************************************!*\
  !*** ./style/ppt_view/ppt-view.svg ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" standalone=\"no\"?>\n<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 20010904//EN\" \"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd\">\n<svg version=\"1.0\" xmlns=\"http://www.w3.org/2000/svg\" width=\"50.000000pt\" height=\"50.000000pt\"\n    viewBox=\"0 0 50.000000 50.000000\" preserveAspectRatio=\"xMidYMid meet\">\n\n    <g transform=\"translate(0.000000,50.000000) scale(0.100000,-0.100000)\" fill=\"#000000\" stroke=\"none\">\n        <path d=\"M52 408 c-8 -8 -12 -54 -12 -140 0 -107 -2 -128 -15 -128 -21 0 -19\n-23 3 -43 16 -15 47 -17 224 -17 186 0 206 2 221 18 21 23 22 42 2 42 -13 0\n-15 21 -15 128 0 86 -4 132 -12 140 -17 17 -379 17 -396 0z m383 -138 l0 -125\n-185 0 -185 0 -3 114 c-1 63 0 121 2 128 4 11 43 13 188 11 l183 -3 0 -125z\nm30 -160 c-8 -14 -422 -14 -430 0 -4 7 70 10 215 10 145 0 219 -3 215 -10z\" />\n        <path d=\"M190 270 l0 -80 53 30 c87 51 84 49 67 60 -8 5 -39 23 -67 40 l-53\n30 0 -80z m60 25 c17 -9 30 -20 30 -25 0 -8 -51 -40 -65 -40 -3 0 -5 18 -5 40\n0 45 0 46 40 25z\" />\n    </g>\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.75aff4d422ee6a6007c4.js.map