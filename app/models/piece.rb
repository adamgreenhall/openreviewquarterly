class Piece < ActiveRecord::Base
  attr_accessible :author_id, :issue_id, :number, :title, :kind, :content, :slug
  validates_presence_of :author_id
  belongs_to :issue
  belongs_to :author
  has_many :illustrations
  before_create :set_slug
  
  def is_published
    self.issue.is_published
  end
  def nice_name
    (self.title.nil? || self.title=='') ? 'Untitled' : self.title
  end
  
  def set_slug
    self.slug = self.get_slug()
  end
  
  def get_slug
    title=(self.title.nil? || self.title=='') ? "untitled #{self.author.name}" : self.title
    URLify.urlify(title, '-')
  end
  
  def author_select(incoming_id_from_form)
    self.author = Author.find(incoming_id_from_form)
  end
  
  def add_illustration_content(illustration)
    illustration_content = IllustrationsContentController.new.content({:@illustration=>illustration})
    content = self.content
    if content.scan('<illustration>').length == 1
      before,_ = *content.split('<illustration>')
      _,after = *content.split('</illustration>')
      self.content = (before.nil? ? '' : before) + illustration_content + (after.nil? ? '' : after)
      self.save()
    else
      self.content+=illustration_content
      self.save()
    end
  end

end
