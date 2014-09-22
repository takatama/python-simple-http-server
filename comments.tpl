<html>
  <head>
    <title>Comments</title>
  </head>
  <body>
    <ul>
% for comment in comments:
      <li>{{str(comment.id)}} : {{comment.comment}} ({{comment.created_at}})</li>
% end
    </ul>
    <form method="POST" action="/comments">
      <input type="text" name="comment">
      <input type="submit">
    </form>
</html>
