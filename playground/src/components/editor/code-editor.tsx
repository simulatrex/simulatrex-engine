import React, { useEffect } from "react";
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/theme-gruvbox_light_hard";
import "./simulatrex-mode";

const CodeEditor = ({
  code,
  setCode,
}: {
  code: string;
  setCode: (code: string) => void;
}) => {
  return (
    <AceEditor
      mode="simulatrex" // Use the custom mode
      theme="light_hard"
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
