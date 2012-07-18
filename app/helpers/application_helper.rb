module ApplicationHelper
  def urlify(name,replaceChar='-')
    URLify.urlify(name,replaceChar)
  end
  def link_to_issue(issue)
    link_to issue.title, urlify(issue.title)
  end
  def link_to_piece(piece,in_issue=false)
    if in_issue
      link_to piece.title, urlify(piece.issue.title)+'/'+urlify(piece.title)
    else
      link_to piece.title, urlify(piece.issue.title)+'#'+urlify(piece.title)
    end
  end
  def link_to_author(author)
    link_to author.name, 'people/'+urlify(author.name)
  end  
end

