module ApplicationHelper
  def urlify(name,replaceChar='-')
    URLify.urlify(name,replaceChar)
  end
end
