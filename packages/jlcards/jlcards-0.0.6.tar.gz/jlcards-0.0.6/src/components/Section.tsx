/* eslint-disable @typescript-eslint/no-unused-vars */
import { PathExt } from "@jupyterlab/coreutils";
import { IDocumentManager } from "@jupyterlab/docmanager";
import { DocumentRegistry } from "@jupyterlab/docregistry";
import { INotebookModel, Notebook } from "@jupyterlab/notebook";
import { Button, Row, Col, Space, Tooltip, Modal } from "antd";
import { enableMapSet } from "immer";
import React, { useEffect } from "react";
import ReactMarkdown from "react-markdown";
import styled from "styled-components";
import { useImmer } from "use-immer";
import { endTag, stages, startTag } from "../constants";
import { generateMarkdown } from "../util";
import { AnnotMap, getAnnotMap } from "../util/mdExtractor";
import { jumpToCell } from "../util/notebook_private";
import QuickFix from "./QuickFix";
import HelpText from "./HelpText";
import { ExclamationCircleOutlined } from '@ant-design/icons';


enableMapSet();

interface ISectionProps {
  notebook: Notebook;
  context: DocumentRegistry.IContext<INotebookModel>;
  docManager: IDocumentManager;
  ServerResponse: JSON;
  handler: any;
}

/** Items in the generated model card */
export interface ISchemaItem {
  /** title of the section */
  title: string;
  /** customized description */
  description: string;
  tooltip: string;
  helpurl: string;
}
export interface ISchemaStageItem extends ISchemaItem {
  cell_ids: number[];
  figures: string[];
}
export interface ISchema {
  modelname: { title: string };
  basicinformation: ISchemaItem;
  intendeduse: ISchemaItem;
  factors: ISchemaItem;
  ethicalconsiderations: ISchemaItem;
  caveatsandrecommendations: ISchemaItem
  author: ISchemaItem;
  datasets: ISchemaItem;
  references: ISchemaItem;
  disaggregatedevaluationresult: ISchemaStageItem;
  libraries: ISchemaItem;
  plotting: ISchemaStageItem;
  datacleaning: ISchemaStageItem;
  preprocessing: ISchemaStageItem;
  hyperparameters: ISchemaStageItem;
  modeltraining: ISchemaStageItem;
  modelevaluation: ISchemaStageItem;
  miscellaneous: ISchemaStageItem;
}
interface ISectionContent {
  notebook: Notebook;
  sectionName: string;
  sectionContent: ISchemaItem | ISchemaStageItem;
  quickFix: React.ReactNode;
}

const getJumpIndex = (sectionName: string, sectionContent: any): number => {
  if (sectionName === "author") {
    return 1;
  }
  // if it's a stage, jump to the top cell if existed
  if (stages.has(sectionName) && sectionContent.cell_ids.length > 0) {
    return sectionContent.cell_ids[0];
  }
  // otherwise insert to top
  return 0;
};
const Bar = styled.div`
  position: relative;
  background: aliceblue;
  width: 40%;
  height: 40px;
  border-radius: 10px;
`;

const VerticalLine: any = styled.div`
  position: absolute;
  left: ${(props: any): string => props.left}%;
  height: 100%;
  width: 5px;
  background-color: lightskyblue;
  border-radius: 15px;
  transition: transform 0.2s, background-color 0.2s;

  &:hover {
    transform: scale(3, 1.5);
    background-color: #1890ff;
    z-index: 2;
    cursor: pointer;
  }
`;

const SectionContent: React.FC<ISectionContent> = ({
  notebook,
  sectionName,
  sectionContent,
  quickFix,
}: ISectionContent) => {
  if (typeof sectionContent !== "object") {
    return null;
  }
  console.log(sectionContent.helpurl, sectionContent.title);
  return (
      <>
        <h1>
          {/* <Tooltip title={sectionContent.tooltip} placement="rightTop"> */}
            {sectionContent.title} {quickFix} <HelpText toolTipContent={sectionContent.tooltip} helpUrl={sectionContent.helpurl}/>
          {/* </Tooltip> */}
        </h1>
        <div style={{ display: "block" }}>
          <ReactMarkdown>{sectionContent.description}</ReactMarkdown>
        </div>
        
        <div style={{ display: "block" }}>
          {sectionName !== "modelname" &&
            "cell_ids" in sectionContent &&
            sectionContent.cell_ids.length > 0 ? (
            <Bar>
              {sectionContent.cell_ids.map((cid: number, idx: number) => (
                <VerticalLine
                  key={idx}
                  left={(cid / notebook.model.cells.length) * 100}
                  onClick={(): void => jumpToCell(notebook, cid - 1)}
                />
              ))}
            </Bar>
          ) : null}
        </div>
        {"figures" in sectionContent
          ? sectionContent.figures.map((src: string, idx: number) => {
            // console.log(sectionName + ' ' + sectionContent.figures.length);
            return (
              <img
                style={{ display: "block" }}
                key={idx}
                src={`data:image/png;base64,${src}`}
              />
            );
          })
          : null}
      </>
  );
};

const Section: React.FC<ISectionProps> = ({
  notebook,
  context,
  docManager,
  ServerResponse,
  handler
}: ISectionProps) => {
  const [annotMap, updateAnnotMap] = useImmer<AnnotMap>(new Map());
  const [data, updateData] = useImmer<ISchema>({} as ISchema);

  useEffect(() => {
    const amap = getAnnotMap(notebook);
    let modelCard: any = JSON.parse(JSON.stringify(ServerResponse));
    amap.forEach((value, key) => {
      if (key in modelCard) {
        modelCard[key]["description"] = value.content;
      }
    });
    updateData(() => modelCard);

    // Add tag for title field
    const titleKey = "modelname";
    if (
      modelCard[titleKey]["description"] !== undefined &&
      !amap.has(titleKey)
    ) {
      const titleCell = notebook.model.cells.get(0).value;
      titleCell.insert(0, `${startTag(titleKey)}\n`);
      titleCell.insert(titleCell.text.length, `\n${endTag(titleKey)}`);
      amap.set(titleKey, {
        idx: 0,
        content: modelCard[titleKey]["description"],
      });
    }
    updateAnnotMap(() => amap);
  }, [notebook]);

  // TODO let user decide the name of the output file
  // TODO test for files in a subdirectory
  return (
    <>
      <Row style={{ position: "sticky", top: 10, float: "right" }}>
        <Space>
          <Col span={6}>
            <Button
              type="primary"
              onClick={(): any => {
                handler();
              }}
            >
              Refresh
            </Button>
          </Col>
          <Col span={6}>
            <Button
              type="primary"
              onClick={(): any => {
                let emptySections = [];
                Object.entries(data).map(
                  ([sectionName, sectionContent]: [string, ISchemaItem], idx: number) => {
                    if (!sectionContent.description) {
                      if (!['#', 'Miscellaneous'].includes(sectionContent.title)) {
                        emptySections.push(sectionContent.title);
                      }
                    }
                  });
                if (emptySections) {
                  Modal.confirm({
                    title: 'The following sections are still empty!',
                    icon: <ExclamationCircleOutlined />,
                    content: [emptySections.join(', '), 'Would you like to add the documentation before exporting?'].join('.\n'),
                    okText: 'Yes',
                    cancelText: 'No (Proceed with exporting)',
                    onOk() {
                    },
                    onCancel() {
                      const dirname = PathExt.dirname(context.path);
                      let fileName = PathExt.basename(context.path);
                      fileName = fileName.split(PathExt.extname(fileName))[0];
                      fileName = fileName.split(" ").join("_");
                      fileName = "card_" + fileName + ".md";
                      const filePath = PathExt.join(dirname, fileName);
                      let mdFile: any = docManager.findWidget(filePath, "Editor");
                      if (mdFile === undefined) {
                        // create the file in the same directory as the notebook
                        mdFile = docManager.createNew(filePath, "Editor");
                      }
                      // console.log(docManager.registry.defaultWidgetFactory(filePath))
                      // docManager.openOrReveal(mdFile.context.path);
                      mdFile.context.ready.then(() => {
                        mdFile.content.model.value.text = generateMarkdown(data);
                      });
                      mdFile.close();
                      docManager.openOrReveal(filePath, 'Markdown Preview');
                    },
                  });
                } else {
                  const dirname = PathExt.dirname(context.path);
                  let fileName = PathExt.basename(context.path);
                  fileName = fileName.split(PathExt.extname(fileName))[0];
                  fileName = fileName.split(" ").join("_");
                  fileName = "card_" + fileName + ".md";
                  const filePath = PathExt.join(dirname, fileName);
                  let mdFile: any = docManager.findWidget(filePath, "Editor");
                  if (mdFile === undefined) {
                    mdFile = docManager.createNew(filePath, "Editor");
                  } 
                  mdFile.context.ready.then(() => {
                    mdFile.content.model.value.text = generateMarkdown(data);
                  });
                  docManager.openOrReveal(filePath, 'Markdown Preview');
                }
              }}
            >
              Export to MD
            </Button>
          </Col>
        </Space>
      </Row>

      {Object.entries(data).map(
        ([sectionName, sectionContent]: [string, ISchemaItem], idx: number) => {
          if (sectionName === "miscellaneous") {
            return null;
          }
          return (
            <SectionContent
              key={idx}
              notebook={notebook}
              sectionName={sectionName}
              sectionContent={sectionContent}
              quickFix={
                <QuickFix
                  sectionName={sectionName}
                  sectionTitle={sectionContent.title}
                  annotMap={annotMap}
                  updateAnnotMap={updateAnnotMap}
                  notebook={notebook}
                  idx={getJumpIndex(sectionName, sectionContent)}
                />
              }
            />
          );
        }
      )}
    </>
  );
};

export default Section;
