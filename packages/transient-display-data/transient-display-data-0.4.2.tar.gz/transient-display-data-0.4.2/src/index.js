// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { ICommandPalette } from '@jupyterlab/apputils';
import { IConsoleTracker } from '@jupyterlab/console';
import { TransientHandler } from './transient';
import { AttachedProperty } from '@lumino/properties';
/**
 * The console widget tracker provider.
 */
export const transient = {
    id: 'vatlab/jupyterlab-extension:transient',
    requires: [IConsoleTracker],
    optional: [ICommandPalette],
    activate: activateTransient,
    autoStart: true
};
export default transient;
function activateTransient(app, tracker, palette) {
    const { shell } = app;
    tracker.widgetAdded.connect((sender, widget) => {
        const console = widget.console;
        const handler = new TransientHandler({
            sessionContext: console.sessionContext,
            parent: console
        });
        Private.transientHandlerProperty.set(console, handler);
        console.disposed.connect(() => {
            handler.dispose();
        });
    });
    const { commands } = app;
    const category = 'Console';
    const toggleShowTransientMessage = 'console:toggle-show-transient-message';
    // Get the current widget and activate unless the args specify otherwise.
    function getCurrent(args) {
        let widget = tracker.currentWidget;
        let activate = args['activate'] !== false;
        if (activate && widget) {
            shell.activateById(widget.id);
        }
        return widget;
    }
    commands.addCommand(toggleShowTransientMessage, {
        label: args => 'Show Transient Messages',
        execute: args => {
            let current = getCurrent(args);
            if (!current) {
                return;
            }
            const handler = Private.transientHandlerProperty.get(current.console);
            if (handler) {
                handler.enabled = !handler.enabled;
            }
        },
        isToggled: () => {
            var _a;
            return tracker.currentWidget !== null &&
                !!((_a = Private.transientHandlerProperty.get(tracker.currentWidget.console)) === null || _a === void 0 ? void 0 : _a.enabled);
        },
        isEnabled: () => tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget
    });
    if (palette) {
        palette.addItem({
            command: toggleShowTransientMessage,
            category,
            args: { isPalette: true }
        });
    }
    app.contextMenu.addItem({
        command: toggleShowTransientMessage,
        selector: '.jp-CodeConsole'
    });
}
/*
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property for a console's transient handler.
     */
    Private.transientHandlerProperty = new AttachedProperty({
        name: 'transientHandler',
        create: () => undefined
    });
})(Private || (Private = {}));
//# sourceMappingURL=index.js.map