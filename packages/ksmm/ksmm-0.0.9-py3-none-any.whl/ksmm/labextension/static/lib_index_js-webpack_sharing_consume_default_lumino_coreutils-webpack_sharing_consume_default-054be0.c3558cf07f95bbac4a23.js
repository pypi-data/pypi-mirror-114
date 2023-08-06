(self["webpackChunk_quansight_jupyterlab_ksmm"] = self["webpackChunk_quansight_jupyterlab_ksmm"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-054be0"],{

/***/ "./lib/components/alerts.js":
/*!**********************************!*\
  !*** ./lib/components/alerts.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SuccessAlertBox": () => (/* binding */ SuccessAlertBox)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_bootstrap_Alert__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-bootstrap/Alert */ "./node_modules/react-bootstrap/esm/Alert.js");


const SuccessAlertBox = (props) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Alert__WEBPACK_IMPORTED_MODULE_1__.default, { variant: "success" },
        "Success ",
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { style: { textDecoration: "underline" }, onClick: () => props.handleClose() }, "Close")));
};


/***/ }),

/***/ "./lib/components/envvar.js":
/*!**********************************!*\
  !*** ./lib/components/envvar.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EnvVarForm": () => (/* binding */ EnvVarForm)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

/*
 * This function is a field that is rendered
 * for the environment variable.
 */
const EnvVarForm = (props) => {
    /*
     * Function to handle a change of key values in a key value store
     */
    const handleKeyChange = (key, newkey) => {
        props.formData[newkey] = props.formData[key];
        delete props.formData[key];
        console.log(props.formData);
    };
    /*
     * Function to handle any changing values
     */
    const handleValueChange = (key, newvalue) => {
        props.formData[key] = newvalue;
        console.log(props.formData);
    };
    const widget = props.uiSchema["ui:widget"];
    const formData = props.formData;
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
        props.properties.map((item) => widget((props = {
            value: item,
            formData: formData,
            handleKey: handleKeyChange,
            handleVal: handleValueChange,
        }))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: (e) => {
                alert(props.onAddClick);
            } }, "Add New")));
};


/***/ }),

/***/ "./lib/components/keyval.js":
/*!**********************************!*\
  !*** ./lib/components/keyval.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KeyValueWidget": () => (/* binding */ KeyValueWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

/*
 * This function has a callback to mutate the formData to
 * add a new 'string':'string' type to the dictionary.
 *
 * Renders a widget for a python dict of
 * { 'string':'string', 'string':'string' }
 */
const KeyValueWidget = (props) => {
    const [key, setKey] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(props.value.name);
    const [val, setVal] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(props.formData[props.value.name]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "string", value: key, onChange: (e) => {
                props.handleKey(key, e.target.value);
                setKey(e.target.value);
            } }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "string", value: val, onChange: (e) => {
                props.handleVal(key, e.target.value);
                setVal(e.target.value);
            } })));
};


/***/ }),

/***/ "./lib/components/kscardgrid.js":
/*!**************************************!*\
  !*** ./lib/components/kscardgrid.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-bootstrap/Card */ "./node_modules/react-bootstrap/esm/Card.js");
/* harmony import */ var react_icons_fa__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-icons/fa */ "./node_modules/react-icons/fa/index.esm.js");
/* harmony import */ var _rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @rjsf/bootstrap-4 */ "webpack/sharing/consume/default/@rjsf/bootstrap-4/@rjsf/bootstrap-4");
/* harmony import */ var _rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _kschema__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../kschema */ "./lib/kschema.js");





const CardGrid = (props) => {
    const { cardPayload, handleSelectKernelspec, handleCopyKernelspec, handleDeleteKernelspec } = props;
    const ksInfo = cardPayload;
    const cardWidget = (props) => {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__.default, { style: {
                width: "18rem",
                height: "12rem",
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__.default.Body, null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__.default.Title, null,
                    "Kernel: ",
                    ksInfo.kernel_name),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__.default.Title, null, ksInfo.jupyter_name)),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__.default.Footer, { className: "align-left" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { style: { cursor: "pointer" }, onClick: () => handleSelectKernelspec(ksInfo.kernel_name) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__.FaRegEdit, null)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { style: { cursor: "pointer" }, onClick: () => handleCopyKernelspec(ksInfo.kernel_name) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__.FaCopy, null)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { style: { cursor: "pointer" }, onClick: () => handleDeleteKernelspec(ksInfo.kernel_name) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__.FaTrash, null)))));
    };
    const uiSchema = {
        "ui:ArrayFieldTemplate": cardWidget,
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement((_rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1___default()), { schema: _kschema__WEBPACK_IMPORTED_MODULE_4__.KsSchema, uiSchema: uiSchema, children: " " })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CardGrid);


/***/ }),

/***/ "./lib/components/ksform.js":
/*!**********************************!*\
  !*** ./lib/components/ksform.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IKsForm": () => (/* binding */ IKsForm)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_bootstrap_Tabs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-bootstrap/Tabs */ "./node_modules/react-bootstrap/esm/Tabs.js");
/* harmony import */ var react_bootstrap_Tab__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-bootstrap/Tab */ "./node_modules/react-bootstrap/esm/Tab.js");
/* harmony import */ var react_bootstrap_Button__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! react-bootstrap/Button */ "./node_modules/react-bootstrap/esm/Button.js");
/* harmony import */ var _rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @rjsf/bootstrap-4 */ "webpack/sharing/consume/default/@rjsf/bootstrap-4/@rjsf/bootstrap-4");
/* harmony import */ var _rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _keyval__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./keyval */ "./lib/components/keyval.js");
/* harmony import */ var _envvar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./envvar */ "./lib/components/envvar.js");
/* harmony import */ var _ksmenu__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./ksmenu */ "./lib/components/ksmenu.js");








const TabMenu = (props) => {
    const [tab, setTab] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)("General Settings");
    /*
     * Generate the menu titles for the schema.
     */
    var menuHeaders = [
        "General Settings",
        "Launch Arguments",
    ];
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Tabs__WEBPACK_IMPORTED_MODULE_2__.default, { defaultActiveKey: menuHeaders[0], onSelect: (k) => setTab(k) }, menuHeaders.map((menuHeader) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Tab__WEBPACK_IMPORTED_MODULE_3__.default, { eventKey: menuHeader, key: menuHeader, title: menuHeader },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ksmenu__WEBPACK_IMPORTED_MODULE_4__.IKsFormGroup, { selecteditem: tab, properties: props.properties, handleAdditionalProperties: props.onAddClick, mainprops: props }))))));
};
const IKsForm = (props) => {
    const uiSchema = {
        "ui:ObjectFieldTemplate": TabMenu,
        env: {
            "ui:widget": _keyval__WEBPACK_IMPORTED_MODULE_5__.KeyValueWidget,
            "ui:autofocus": true,
            "ui:ObjectFieldTemplate": _envvar__WEBPACK_IMPORTED_MODULE_6__.EnvVarForm,
            "ui:options": {
                expandable: true,
            },
        },
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement((_rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1___default()), { schema: props.schema, uiSchema: uiSchema, formData: props.formData, onSubmit: props.onSubmit }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Button__WEBPACK_IMPORTED_MODULE_7__.default, { variant: "secondary", onClick: () => props.onCancel() }, "Cancel")));
};


/***/ }),

/***/ "./lib/components/ksmenu.js":
/*!**********************************!*\
  !*** ./lib/components/ksmenu.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IKsFormGroup": () => (/* binding */ IKsFormGroup)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

/*
 * This is a nested component in the FieldTemplate, and
 * does all the work for rendering the different options in their
 * respective places.
 *
 * props: data -> The data to render - namely, the data as defined in the schema
 */
const IKsFormGroup = (props) => {
    const fg = generateFormGroupMap(props.properties);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, fg[props.selecteditem].map((index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "property-wrapper", key: index }, props.properties[index].content)))));
};
/*
 * Grab the location of the element in the array,
 * returning a value of the positions in the array.
 */
function generateFormGroupMap(dataArr) {
    const GeneralSettingsArray = [];
    const LaunchArgumentsArray = [];
    const EnvironmentVariableArray = [];
    const ComputeParametersArray = [];
    const MetadataArray = [];
    dataArr.forEach((element) => {
        if (element.name == "display_name" ||
            element.name == "interrupt_mode" ||
            element.name == "language") {
            GeneralSettingsArray.push(dataArr.indexOf(element));
        }
        else if (element.name == "argv") {
            LaunchArgumentsArray.push(dataArr.indexOf(element));
        }
        else if (element.name == "env") {
            EnvironmentVariableArray.push(dataArr.indexOf(element));
        }
        else if (element.name == "parameters") {
            ComputeParametersArray.push(dataArr.indexOf(element));
        }
        else if (element.name == "metadata") {
            MetadataArray.push(dataArr.indexOf(element));
        }
        else {
            console.log("Unknown element name", element.name);
        }
    });
    return {
        ["General Settings"]: GeneralSettingsArray,
        ["Launch Arguments"]: LaunchArgumentsArray,
        ["Environment Variables"]: EnvironmentVariableArray,
        ["Compute Parameters"]: ComputeParametersArray,
        ["Metadata"]: MetadataArray,
    };
}


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'ksmm', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components_lib_icon_iconimports__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components/lib/icon/iconimports */ "./node_modules/@jupyterlab/ui-components/lib/icon/iconimports.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");




/*
 * The command IDs used by the to create a kernelspec.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = "ksmm:create-kernelspec";
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the ksmm extension.
 */
const ksmmExtension = {
    id: "jupyterlab-ksmm-plugin",
    autoStart: true,
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher],
    activate: (app, launcher) => {
        const { commands } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: "A way to manage Kernelspecs",
            label: "Kernelspec Management",
            icon: (args) => (args['isPalette'] ? null : _jupyterlab_ui_components_lib_icon_iconimports__WEBPACK_IMPORTED_MODULE_2__.extensionIcon),
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_3__.KernelspecManagerWidget();
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                widget.title.label = "Kernelspec Management";
                app.shell.add(widget, "main");
            }
        });
        if (launcher) {
            launcher.add({
                command
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ksmmExtension);


/***/ }),

/***/ "./lib/kschema.js":
/*!************************!*\
  !*** ./lib/kschema.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KsSchema": () => (/* binding */ KsSchema)
/* harmony export */ });
/*
 * This file is a special file that houses
 * the schema definitions for this entire application.
 *
 * rjsf is used effectively throughout the application for many purposes,
 * and then can be edited for form edits.
 */
/*
export const fetchMachineParameters = () => {
  // TODO: remove and use jupyterlab service URL.
  const url =  document.location.origin+"/parameters";
  const machineParameters = async () => {
    const response = await fetch(url);
    const jsondata = await response.json();
    console.log(jsondata);
  };
  machineParameters();
};
fetchMachineParameters();
*/
/*
 * The following schema complies to IPython Kernel
 * Standards. When making changes, note that the UI
 * is also subject to change based on the types.
 */
// export const IPySchema: JSONSchema7 = {
//   title: "Kernelspec Management Menu",
//   type: "object",
//   properties: {
//     argv: { type: "array", items: { type: "string" }, title: "" },
//     env: {
//       type: "object",
//       title: "object",
//       properties: {
//         EnvVar: { type: "string" },
//       },
//       additionalProperties: {
//         type: "string",
//       },
//     },
//     display_name: { type: "string", title: "Display Name" },
//     language: { type: "string", title: "Programming Language" },
//     interrupt_mode: {
//       type: "string",
//       title: "Interrupt Mode",
//       enum: ["signal", "message"],
//     },
//     parameters: {
//       type: "object",
//       properties: {
//         cores: { type: "string", enum: ["4", "6", "8"], title: "CPU Cores" },
//         memory: {
//           type: "string",
//           enum: ["8GB", "16GB", "32GB"],
//           title: "Memory",
//         },
//       },
//     },
//     metadata: { type: "object", title: "" },
//   },
//   required: [
//     "argv",
//     "display_name",
//     "env",
//     "interrupt_mode",
//     "language",
//     "metadata",
//   ],
// }
/*
 * This is the schema for the display cards rendered for
 * each kernel. It can be obtained by using the generation
 * function. When called on the ipyschema object, the function
 * returns a ipyCardSchema.
 */
const KsSchema = {
    title: "Kernelspec Card",
    type: "array",
    items: {
        type: "object",
        properties: {
            kernel_name: { type: "string" },
            jupyter_name: { type: "string" },
        },
    },
};


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelspecManagerWidget": () => (/* binding */ KernelspecManagerWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_bootstrap_Container__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react-bootstrap/Container */ "./node_modules/react-bootstrap/esm/Container.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _components_kscardgrid__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/kscardgrid */ "./lib/components/kscardgrid.js");
/* harmony import */ var _components_alerts__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/alerts */ "./lib/components/alerts.js");
/* harmony import */ var _components_ksform__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/ksform */ "./lib/components/ksform.js");
/* harmony import */ var bootstrap_dist_css_bootstrap_min_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");



// import { JSONSchema7 } from "json-schema";





/**
 * React component for listing the possible
 * ipykernel options.
 *
 * @returns The React component.
 */
const KernelManagerComponent = () => {
    const [data, setData] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({});
    const [showForm, setShowForm] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [kernelFormData, setKernelFormData] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({});
    const [selectedKernelName, setSelectedKernelName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)("");
    const [cardData, setCardData] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [alertBox, setAlertBox] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [schema, setSchema] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({});
    /**
     * Handles the Kernel Selection
     * at the select screen. ,
     */
    const handleSelectKernelspec = (kernelName) => {
        setSelectedKernelName(kernelName);
        setKernelFormData(data[kernelName]);
        setShowForm(true);
    };
    /**
     * Return Home on click.
     * TODO: Add Guards to check if editing.
     */
    const handleGoHome = () => {
        setShowForm(false);
        setAlertBox(false);
    };
    const refreshSchemas = () => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)("/schema", {
            method: "GET",
        }).then((s) => {
            setSchema(s);
        });
    };
    const refreshKernelspecs = () => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)("/", {
            method: "GET",
        }).then((res) => {
            setData(res);
            setCardData(createCardData(res));
        });
    };
    const handleCopyKernelspec = (kernel_name) => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)("/copy", {
            method: "POST",
            body: JSON.stringify({ name: kernel_name }),
        }).then((data) => {
            alert("A copy of " + kernel_name + " has been created.");
            refreshKernelspecs();
        });
    };
    const handleDeleteKernelspec = (kernel_name) => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)("/delete", {
            method: "POST",
            body: JSON.stringify({ name: kernel_name }),
        }).then((data) => {
            alert(kernel_name + " has been deleted.");
            refreshKernelspecs();
        });
    };
    /**
     * Handles a form submission when
     * kernels are modified in any form.
     *
     * Passed as a prop to Form
     */
    const handleSubmitKernelspec = (e) => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)("/", {
            method: "POST",
            body: JSON.stringify({
                editedKernelPayload: JSON.stringify(e.formData),
                originalKernelName: selectedKernelName,
            }),
        }).then((data) => {
            if (data.success) {
                setAlertBox(true);
                refreshKernelspecs();
                setKernelFormData(e.formData);
            }
        });
    };
    /**
     * Generate the package of data needed
     * to display at the card selection screen.
     *
     * This method is called on when then data is generated to
     * send into the method generating the card data.
     */
    const createCardData = (ks) => {
        var arr = new Array();
        for (const property in ks) {
            arr.push({
                kernel_name: `${property}`,
                jupyter_name: `${ks[property].display_name}`,
            });
        }
        return arr;
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        refreshSchemas();
        refreshKernelspecs();
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Container__WEBPACK_IMPORTED_MODULE_4__.default, { fluid: true },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, "Kernelspec Manager"),
        !showForm &&
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: {
                    display: "flex",
                    flexWrap: "wrap"
                } }, cardData.map((cardPayload, idx) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_kscardgrid__WEBPACK_IMPORTED_MODULE_5__.default, { handleSelectKernelspec: handleSelectKernelspec.bind(undefined), handleCopyKernelspec: handleCopyKernelspec.bind(undefined), handleDeleteKernelspec: handleDeleteKernelspec.bind(undefined), cardPayload: cardPayload, key: idx })))),
        alertBox && react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_alerts__WEBPACK_IMPORTED_MODULE_6__.SuccessAlertBox, { handleClose: handleGoHome }),
        showForm && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_ksform__WEBPACK_IMPORTED_MODULE_7__.IKsForm, { schema: schema, formData: kernelFormData, onSubmit: handleSubmitKernelspec.bind(undefined), onCancel: handleGoHome.bind(undefined) }))));
};
/**
 * KernelspecManagerWidget main class.
 */
class KernelspecManagerWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor() {
        super();
        this.addClass("jp-Ksmm");
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(KernelManagerComponent, null);
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-054be0.c3558cf07f95bbac4a23.js.map