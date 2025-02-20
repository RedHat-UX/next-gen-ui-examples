import { useRef, useLayoutEffect } from 'react';

/**
 * Red Hat Design System componetn (web components)
 * @param param0 
 * @returns 
 */
export function RHDSComponent({ markup }: { markup: string }) {
    const elRef = useRef<HTMLDivElement>(null);

    useLayoutEffect(() => {
        if (!elRef.current) {
            return;
        }

        const range = document.createRange();
        range.selectNode(elRef?.current);
        const documentFragment = range.createContextualFragment(markup);

        // Inject the markup, triggering a re-run! 
        elRef.current.innerHTML = '';
        elRef?.current?.append(documentFragment);
    }, []);

    return (
        <div
            ref={elRef}
            dangerouslySetInnerHTML={{ __html: markup }}>
        </div>
    );
}
