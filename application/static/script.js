document.addEventListener('DOMContentLoaded', () => {
  // Functionality for message flash close button
  (document.querySelectorAll('.notification .delete') || []).forEach(
    $delete => {
      const $notification = $delete.parentNode;

      $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
      });
    }
  );

  document.querySelectorAll('.button :not(.edit-button)').forEach(btn =>
    btn.addEventListener('click', () => {
      btn.classList.add('is-loading');
    })
  );

  document.querySelectorAll('.edit-button').forEach(btn => {
    btn.addEventListener('click', () => {
      const msgKey = btn.closest('.card').id;
      fetch('/user-page', {
        headers: {
          'Content-Type': 'pplication/json',
        },
        method: 'POST',
        body: JSON.stringify({
          key: msgKey,
        }),
      }).then(function (response) {
        document.cookies = `message_key=${msgKey}`;
        return response.text();
      });
    });
  });

  (
    document.querySelector('#file-upload input[type=file]') || []
  ).onchange = () => {
    if (fileInput.files.length > 0) {
      const fileName = document.querySelector('#file-upload .file-name');
      fileName.textContent = fileInput.files[0].name;
    }
  };
});
a;
