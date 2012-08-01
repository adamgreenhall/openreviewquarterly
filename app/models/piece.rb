class Piece < ActiveRecord::Base
  attr_accessible :author_id, :issue_id, :number, :title, :kind, :content
  validates_presence_of :title, :author_id
  belongs_to :issue
  belongs_to :author
  has_many :illustrations
  def is_published
    self.issue.is_published
  end
  def nice_name
    (self.title.nil? || self.title=='') ? 'Untitled' : self.title
  end
  
  def url
    title=(self.title.nil? || self.title=='') ? "untitled #{self.author.name}" : self.title
    URLify.urlify(title, '-')
  end
  
  def author_select(incoming_id_from_form)
    self.author = Author.find(incoming_id_from_form)
  end

end
