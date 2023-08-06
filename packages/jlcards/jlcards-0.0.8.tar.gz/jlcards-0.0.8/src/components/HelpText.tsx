import React from 'react';
import { Button } from 'antd';

export interface IHelpText {
    toolTipContent: string;
    helpUrl: string[];
}

const HelpText: React.FC<IHelpText> = ({
    toolTipContent,
    helpUrl
}: IHelpText) => {
    if (helpUrl && helpUrl.length > 0) {
        let urls = [];
        helpUrl.forEach((url, idx) => {
            urls.push(<Button type="link" style={{ padding: "1px" }} onClick={() => { window.open(url) }}>[Example {idx + 1}]</Button>);
        });
        return (<>
            {urls}
            </>
        )
    } else {
        return null;
    }
};


export default HelpText;