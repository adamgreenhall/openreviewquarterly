module IssuesHelper
  def issue_cover(issue)
    image_tag('covers/'+urlify(issue.title)+'.jpg')
  end
  def issue_link(issue)
    link_to issue.title,urlify(issue.title)
  end
end
