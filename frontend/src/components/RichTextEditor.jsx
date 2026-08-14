import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Placeholder from '@tiptap/extension-placeholder';
import { useEffect } from 'react';
import './RichTextEditor.css';

/**
 * Qayta ishlatiladigan rich text editor.
 * `value` — HTML matn (masalan "<p>Salom <strong>dunyo</strong></p>")
 * `onChange` — matn o'zgarganda chaqiriladi, yangi HTML'ni beradi
 */
function RichTextEditor({ value, onChange, placeholder }) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({ placeholder: placeholder || 'Yozing...' }),
    ],
    content: value || '',
    onUpdate: ({ editor }) => {
      onChange(editor.getHTML());
    },
  });

  // Agar tashqaridan `value` o'zgartirilsa (masalan formani tozalash),
  // editor ichidagi matnni ham yangilaymiz
  useEffect(() => {
    if (editor && value !== editor.getHTML()) {
      editor.commands.setContent(value || '');
    }
  }, [value]);

  if (!editor) return null;

  return (
    <div className="rich-editor">
      <div className="rich-editor-toolbar">
        <button
          type="button"
          className={editor.isActive('bold') ? 'active' : ''}
          onClick={() => editor.chain().focus().toggleBold().run()}
        >
          <b>B</b>
        </button>
        <button
          type="button"
          className={editor.isActive('italic') ? 'active' : ''}
          onClick={() => editor.chain().focus().toggleItalic().run()}
        >
          <i>I</i>
        </button>
        <button
          type="button"
          className={editor.isActive('bulletList') ? 'active' : ''}
          onClick={() => editor.chain().focus().toggleBulletList().run()}
        >
          • Ro'yxat
        </button>
      </div>
      <EditorContent editor={editor} className="rich-editor-content" />
    </div>
  );
}

export default RichTextEditor;