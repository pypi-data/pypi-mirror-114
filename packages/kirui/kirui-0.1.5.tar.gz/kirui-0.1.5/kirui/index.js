import { Component } from './core/component';
import { registry } from './core/registry';

import { App } from './components/base/app';

export { App, Component, registry };

/* Layout */
import { TopBarLayout, TopBarHeader, TopBarBody } from './components/layout/topbar';
export { TopBarLayout, TopBarHeader, TopBarBody };
export { SidebarLayout, SidebarHeader, SidebarMenu } from './components/layout/sidebar';

/* Modalsfsd */
import { SideModal, ModalHeader, ModalBody, ModalFooter, ModalLink } from './components/modal';
export { SideModal, ModalHeader, ModalBody, ModalFooter, ModalLink };

/* Form */
import { Form } from './components/form/form';
import { FormField } from './components/form/field';
import { Input, MultiSelectCheckbox, CheckboxSwitch } from './components/form/widget/index';
export { FormField, Input, Form, MultiSelectCheckbox, CheckboxSwitch }

/* Table */
import { KrTable } from './components/table/main';
import { KrColumns, KrColumn } from './components/table/columns';
import { KrRows, KrRow, KrCell } from './components/table/rows';
export { KrTable, KrColumns, KrColumn, KrRows, KrRow, KrCell }

/* Panel */
import { KrAjaxPanel } from './components/panel/ajax';
export { KrAjaxPanel }

import $ from 'jquery';
import { h, render } from 'preact';
$(document).ready(function () {
  /*$.get({
      url: '/backend/data/',
      contentType: "application/json",
      success: function (root) {

      }
  });*/

    Component.prototype.dataToCreateElement([$app_data]);
    const app = h(...$app_data);
    render(app, document.getElementById('app'), document.getElementById('app'));
});
