import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { ToolbarButton } from '@jupyterlab/apputils';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { NotebookPanel, INotebookModel } from '@jupyterlab/notebook';


function JupyterLabLineWrapCellOuputOn() {
  var divs = document.querySelectorAll(".jp-OutputArea-output pre");
  for(let i=0; i<divs.length; i++) {
    var div = divs[i] as HTMLElement;
    if (div.style['whiteSpace'] != "pre") div.style["whiteSpace"] = "pre";
  }
}

function JupyterLabLineWrapCellOuputOff() {
  var divs = document.querySelectorAll(".jp-OutputArea-output pre");
  for(let i=0; i<divs.length; i++) {
    var div = divs[i] as HTMLElement;
    if (div.style['whiteSpace'] != "pre-wrap") div.style["whiteSpace"] = "pre-wrap";
  }
}


/**
 * Initialization data for the jupyterlab_linewrapcelloutput extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_linewrapcelloutput:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyterlab_linewrapcelloutput is activated!');
    app.docRegistry.addWidgetExtension('Notebook', new ButtonLineWrapCellOutput());
  }
};

export class ButtonLineWrapCellOutput
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
  {
    createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
      
      
      const triggerLineWrapCellOutput = () => {
        if (SET) {
          SET = false;
          if (button.hasClass('selected')) button.removeClass('selected');
          clearInterval(t);
          JupyterLabLineWrapCellOuputOff();
        }
        else {
          SET = true;
          button.addClass('selected');
          t = setInterval(JupyterLabLineWrapCellOuputOn,10);
        }
      };

      const button = new ToolbarButton({
        className: 'buttonLineWrapCellOuput',
        iconClass: 'wll-WrapIcon',
        label: 'wrap',
        onClick: triggerLineWrapCellOutput,
        tooltip: 'Line Wrap Cell Ouput'
      })

      panel.toolbar.insertItem(10, 'LineWrapCellOutput', button);

      var SET = true;
      var t = setInterval(JupyterLabLineWrapCellOuputOn,10);
      button.addClass('selected');
      return new DisposableDelegate(() => { button.dispose(); });
    }
  }

export default plugin;