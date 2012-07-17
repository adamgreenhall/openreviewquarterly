module IssuesHelper
  def issue_cover(issue)
    image_tag('covers/'+urlify(issue.title)+'.jpg')
  end
end
