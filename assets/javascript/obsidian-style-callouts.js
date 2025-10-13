function renderObsidianCallouts() {
    console.log("📦 Running Obsidian callout processor...");

    const calloutTypeMap = {
        note: "note",

        abstract: "abstract",
        summary: "abstract",
        tldr: "abstract",

        info: "info",
        todo: "info",

        tip: "tip",
        hint: "tip",
        important: "tip",

        success: "success",
        check: "success",
        done: "success",

        question: "question",
        help: "question",
        faq: "question",

        warning: "warning",
        caution: "warning",
        attention: "warning",

        failure: "failure",
        fail: "failure",
        missing: "failure",

        danger: "danger",
        error: "danger",

        bug: "bug",

        example: "example",

        quote: "quote",
        cite: "quote",

        statblock: "statblock"
    };

    const calloutIcons = {
        note: "fa-solid fa-pen",
        abstract: "fa-solid fa-file-lines",
        info: "fa-solid fa-circle-info",
        tip: "fa-solid fa-fire",
        success: "fa-solid fa-check",
        question: "fa-solid fa-question-circle",
        warning: "fa-solid fa-triangle-exclamation",
        failure: "fa-solid fa-xmark",
        danger: "fa-solid fa-bolt",
        bug: "fa-solid fa-bug",
        example: "fa-solid fa-list",
        quote: "fa-solid fa-quote-left",
        statblock: "fa-solid fa-dice-d20"
    };

    function convertInlineMarkdown(text) {
        const escapeHtml = (str) =>
            str.replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");

        const escaped = escapeHtml(text);

        return escaped
            // bold: **text**
            .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
            // italic: *text*
            .replace(/\*(.+?)\*/g, "<em>$1</em>")
            // underline: __text__
            .replace(/__(.+?)__/g, "<u>$1</u>")
            // strikethrough: ~~text~~ (optional)
            .replace(/~~(.+?)~~/g, "<s>$1</s>");
    }



    document.querySelectorAll("blockquote").forEach((block) => {
        const blockText = block.textContent.trim();

        console.log("🧪 Blockquote candidate:", blockText);
        if (!blockText.startsWith("[!")) return;
        console.log("✅ Matched callout block:", blockText);


        if (block.classList.contains("obsidian-callout-processed")) return;

        const calloutChunks = [];
        let currentChunk = null;

        const rawHtml = block.innerHTML;
        const lines = rawHtml.split(/<br\s*\/?>|\n/);


        lines.forEach((line) => {
            const div = document.createElement("div");
            div.innerHTML = line;
            const text = div.innerText.trim();

            const match = text.match(/^\[!(\w+)\](-?)\s*(.+)$/);
            if (match) {
                if (currentChunk) calloutChunks.push(currentChunk);
                const rawType = match[1].toLowerCase();
                const type = calloutTypeMap[rawType] || "note";
                const collapsed = match[2] === "-";
                const title = match[3];
                currentChunk = {
                    type,
                    collapsedByDefault: collapsed,
                    title,
                    content: [],
                };
            } else if (currentChunk && text !== "") {
                const p = document.createElement("p");
                const lineText = line.trim();

                // Convert lines like "Traits" or "Actions" into headers
                if (/^(Traits|Actions|Reactions|Legendary Actions|Lair Actions)\s*[:¶]?$/.test(lineText)) {
                    const h = document.createElement("h3");
                    h.textContent = lineText.replace(/[:¶]$/, '');
                    currentChunk.content.push(h);
                } else {
                    const p = document.createElement("p");
                    const isPlain = !/[<>]/.test(lineText); // skip markdown conversion if tags exist
                    p.innerHTML = isPlain ? convertInlineMarkdown(lineText) : lineText;
                    currentChunk.content.push(p);

                }


            }
        });

        if (currentChunk) calloutChunks.push(currentChunk);

        const container = document.createElement("div");

        calloutChunks.forEach(({ type, collapsedByDefault, title, content }) => {
            const wrapper = document.createElement("div");
            wrapper.className = `obsidian-callout callout-${type}`;
            wrapper.style.borderLeft = "4px solid var(--callout-border, #888)";
            wrapper.style.background = "var(--callout-bg, #f9f9f9)";
            wrapper.style.margin = "1em 0";
            wrapper.style.padding = "0.75em 1em";
            wrapper.style.position = "relative";

            const contentDiv = document.createElement("div");
            contentDiv.className = "callout-content";
            content.forEach((node) => contentDiv.appendChild(node));
            contentDiv.style.display = collapsedByDefault ? "none" : "";

            const header = document.createElement("div");
            header.className = "callout-header";
            header.style.fontWeight = "bold";
            header.style.cursor = collapsedByDefault ? "pointer" : "default";
            header.style.display = "flex";
            header.style.alignItems = "center";
            header.style.gap = "0.5em";
            header.style.userSelect = "none";

            const icon = document.createElement("i");
            icon.className = calloutIcons[type] || "fa-solid fa-message";
            icon.classList.add("callout-icon");

            const titleSpan = document.createElement("span");
            titleSpan.textContent = title;

            const arrow = document.createElement("span");
            arrow.className = "callout-arrow";
            arrow.textContent = collapsedByDefault ? "▸" : "▾";
            arrow.style.fontSize = "1em";
            arrow.style.paddingLeft = "0.25em";
            arrow.style.display = collapsedByDefault ? "inline" : "none";

            if (collapsedByDefault) {
                header.addEventListener("click", () => {
                    const isVisible = contentDiv.style.display !== "none";
                    contentDiv.style.display = isVisible ? "none" : "";
                    arrow.textContent = isVisible ? "▸" : "▾";
                });
            }

            header.appendChild(icon);
            header.appendChild(titleSpan);
            header.appendChild(arrow);

            wrapper.appendChild(header);
            wrapper.appendChild(contentDiv);
            container.appendChild(wrapper);
        });

        block.classList.add("obsidian-callout-processed");
        block.replaceWith(container);
    });
}

if (typeof document$ !== "undefined") {
    document$.subscribe(() => renderObsidianCallouts());
} else {
    if (document.readyState !== "loading") {
        renderObsidianCallouts();
    } else {
        document.addEventListener("DOMContentLoaded", renderObsidianCallouts);
    }
}
