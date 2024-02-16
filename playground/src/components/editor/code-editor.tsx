import React from "react";
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-java";
import "ace-builds/src-noconflict/theme-github";

const CodeEditor = ({
  code,
  setCode,
}: {
  code: string;
  setCode: (code: string) => void;
}) => {
  return (
    <AceEditor
      mode="java" // Java mode for simple highlighting, create a custom mode for your DSL if needed
      theme={
        typeof window !== "undefined" &&
        window.document.body.classList.contains("dark")
          ? "monokai"
          : "github"
      }
      onChange={setCode}
      name="code-editor"
      editorProps={{ $blockScrolling: true }}
      value={code}
      setOptions={{
        enableBasicAutocompletion: true,
        enableLiveAutocompletion: true,
        enableSnippets: true,
        showLineNumbers: true,
        tabSize: 2,
      }}
      style={{ width: "100%", height: "100%" }}
    />
  );
};

export default CodeEditor;
