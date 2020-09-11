git ls-remote origin 'pull/*/head' | awk '{print $2}' |
while read ref; do
  pr=$(echo $ref | cut -d/ -f3)
  git fetch origin $ref > /dev/null
  files_changed=$(git show --pretty=format:'' --name-only FETCH_HEAD|wc -l)
  echo "PR number $pr has changes in $files_changed files"
done