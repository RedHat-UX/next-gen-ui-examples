'use client'

import { ToolCallContentPartComponent } from '@assistant-ui/react';
import { CheckIcon, ChevronDownIcon, ChevronUpIcon } from 'lucide-react';
import { useState } from "react";
import { Button } from "../ui/button";
import { RHDSComponent } from '../RHDSComponent';

export const ToolFallback: ToolCallContentPartComponent = (part) => {
    const [isCollapsed, setIsCollapsed] = useState(true);
    let content = part.result;
    if (content && content !== "") {
        try {
            content = JSON.parse(part.result);
            content = JSON.stringify(content, null, 2);
        } catch (e) {
        }
        if (part.status.type === "complete") {
            console.log(content)
        }
    }
    let className = part.toolName;
    className += " " + (part.toolName.startsWith('genie') ? "genie" : "not_genie");

    return (
        <div id="tool-message" className={className}>
            <div id="tool-debug" className="mb-4 flex w-full flex-col gap-3 rounded-lg border py-3">
                <div className="flex items-center gap-2 px-4">
                    <CheckIcon className="size-4" />
                    <p className="">
                        Used tool (Debug): <b>{part.toolName}</b>
                    </p>
                    <div className="flex-grow" />
                    <Button onClick={() => setIsCollapsed(!isCollapsed)}>
                        {isCollapsed ? <ChevronUpIcon /> : <ChevronDownIcon />}
                    </Button>
                </div>
                {!isCollapsed && (
                    <div className="flex flex-col gap-2 border-t pt-2">
                        <div className="px-4">
                            <pre className="whitespace-pre-wrap">Args: {part.argsText}</pre>
                        </div>
                        {part.result !== undefined && (
                            <div className="border-t border-dashed px-4 pt-2">
                                <p className="font-semibold">Result:</p>
                                <pre className="whitespace-pre-wrap">
                                    {content}
                                </pre>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {part.toolName.startsWith('genie_rhds') && part.result &&
                <section aria-labelledby="prescriptive-ui" id="genie_component">
                    {part.result && <RHDSComponent markup={part.result}></RHDSComponent>}
                </section>
            }
            {part.toolName.startsWith('genie_patternfly') && part.result &&
                <section aria-labelledby="prescriptive-ui" id="genie_component">
                    NOT IMPLEMENTED!!!
                </section>
            }
        </div>
    );
};