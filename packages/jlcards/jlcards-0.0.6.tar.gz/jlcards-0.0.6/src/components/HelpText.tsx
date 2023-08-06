import React from 'react';
import { InfoCircleTwoTone } from '@ant-design/icons';
import { Tooltip } from "antd";


export interface IHelpText {
    toolTipContent: string;
    helpUrl: string;
}


const HelpText: React.FC<IHelpText> = ({
    toolTipContent,
    helpUrl
}: IHelpText) => {
    if (helpUrl && helpUrl.length > 0) {
        return (
            <Tooltip title={toolTipContent} placement="rightTop">
                <InfoCircleTwoTone onClick={() => {
                    window.open(helpUrl);
                }} />
            </Tooltip>)
    } else {
        return (
            <Tooltip title={toolTipContent} placement="rightTop">
                <InfoCircleTwoTone />
            </Tooltip>)
    }
};


export default HelpText;